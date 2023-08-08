import asyncio
from pyppeteer import launch
import csv
import time
import os

'''
Input: URL of the page containing list of all movies/tvs
Output: This returns individual URLs of the title page, videopage, and chunk of each movie/tv
'''

profile_path = '/Users/abdullah/Library/Application Support/Google/Chrome/Default'
exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

urls_main_top = {
    'all' : 'https://www.pbs.org/shows/?search=&genre=all-genres&source=all-sources&sortBy=popular&stationId=bf21732a-f52f-46ca-bbb6-4ae9663a94bf'
}


async def get_url_of_vidchunk(url):
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    chunk_url = [""]

    def interception_fun(response):
        if (".ts" in response.url and "video" in response.url) or (".m4s" in response.url and "segment_" in response.url and "video" in response.url):
            # Response logic goes here
            print("URL:", response.url, "\n")
            chunk_url[0] = response.url
            #print("Method:", response.request.method)
            #print("Response headers:", response.headers)
            #print("Request Headers:", response.request.headers)
            #print("Response status:", response.status)
        return
    
    try:
        page = await browser.newPage()
        await page.goto(url)
        page.on('response', interception_fun)

        await page.waitForSelector('body')

        # Find the iframe element by its class name
        iframe_selector = '.video-player__iframe'
        iframe_element = await page.waitForSelector(iframe_selector)

        # Switch to the iframe
        iframe = await iframe_element.contentFrame()

        # Find the video element within the iframe
        video_selector = 'video'
        video_element = await iframe.waitForSelector(video_selector)

        # Play the video
        await iframe.evaluate('(video) => video.play()', video_element)

        start_time = time.time()
        elapsed_time = 0
        while True:
            if chunk_url[0] != "":
                break
            else:
                #await page.waitFor(1000) # load page for 1 more sec
                await asyncio.sleep(1)
            
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 3: # max timeout
                break

    except Exception as e:
        print(url,"\n",e)
    
    await browser.close()
    print(f"returning --> {chunk_url[0]}\n")
    return chunk_url[0]


async def get_video_links(url):
    print(url)
    video_links = []
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    page = await browser.newPage()
    await page.goto(url)
    link_data = await page.evaluate('''() => {
        const links = Array.from(document.querySelectorAll('[href]'));
        const data = links.map(link => {
            return {
                href: link.href,
                text: link.textContent.trim()
            };
        });
        return data;
    }''')

    for data in link_data:
            if "www.pbs.org/video/" in data['href']:
                print(data['href'])
                video_links.append(data['href'])

    await browser.close()
    return video_links


async def scroll_to_bottom(page, increment=700):
    all_link_data = []
    shows_count = 0
    MAX_SHOWS = 5 ### CHANGE IT !!!!
    
    while True:
        link_data = await page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('[href]'));
            const data = links.map(link => {
                return {
                    href: link.href,
                    text: link.textContent.trim()
                };
            });
            return data;
        }''')
        
        previous_scroll = await page.evaluate('window.scrollY')
        target_scroll = previous_scroll + increment
        await page.evaluate(f'window.scrollTo(0, {target_scroll})')  # Corrected interpolation
        
        await asyncio.sleep(2)  # Adjust the sleep time as needed
        
        current_scroll = await page.evaluate('window.scrollY')

        for data in link_data:
            if "https://www.pbs.org/show/" in data['href']:
                print(data['href'])
                shows_count += 1
                all_link_data.append(data)

        print(f"current_scroll={current_scroll}, previous_scroll={previous_scroll}")
        if current_scroll == previous_scroll or shows_count >= MAX_SHOWS:
            return all_link_data[:MAX_SHOWS]

    

async def get_link_addresses(url):
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    page = await browser.newPage()
    await page.goto(url)
    
    all_link_data = await scroll_to_bottom(page)

    await browser.close()
    return all_link_data


async def get_all_links(url):
    all_link_data = await get_link_addresses(url)
    all_link_data_new = [] # removes duplicates, add videopage url

    for data in all_link_data:
        name = data['text']
        url_title = data['href']
        url_videopage = ''
        data_new = {'name':name, 'url_titlepage':url_title, 'url_videopage': url_videopage}
        all_link_data_new.append(data_new)
            
    return all_link_data_new


if __name__ == '__main__':
    count_dict = {}
    keys = ['name', 'url_titlepage', 'url_videopage', 'url_chunk','content']
    
    # Check if the file exists
    if not os.path.exists("already_collected.txt"):
        # Create the file if it doesn't exist
        with open("already_collected.txt", 'w') as already_file:
            already_file.write("already_collected.txt\n")
    
    already_collected = open("already_collected.txt").readlines()

    start_time = time.time()
    elapsed_time = 0

    for content, main_url in urls_main_top.items():
        print("\n"*10, "*"*25, f"{content}", "*"*25, "\n\n")
        all_link_data_new = asyncio.get_event_loop().run_until_complete(get_all_links(main_url))
        count_dict[content] = len(all_link_data_new)
        print(f"{content} = {len(all_link_data_new)}")

        count = 0  
        print("\n\n")
        for data in all_link_data_new:
            count += 1
            name = data['url_titlepage'].rsplit("/", 2)[-2]
            data['name'] = name
            print(f"**** {count} out of {len(all_link_data_new)} --- {content} ~~~ elapsed: {elapsed_time} min ****")

            current_time = time.time()
            elapsed_time = int((current_time - start_time)//60)

            if name+"\n" in already_collected:
                print(f"{name} is already collected!\n\n\n\n\n\n")
                continue
        
            ####
            video_links = asyncio.get_event_loop().run_until_complete(get_video_links(data['url_titlepage']))

            for video_link in video_links:
                print(video_link)
                url_chunk = asyncio.get_event_loop().run_until_complete(get_url_of_vidchunk(video_link))
                if url_chunk:
                    data['url_videopage'] = video_link
                    break
            ###

            if url_chunk == "":
                print(f"failed to get url_chunk of {name}\n")


            url_titlepage = data['url_titlepage']
            url_videopage = data['url_videopage']
            
            print("Name:", name)
            print("Titlepage:", url_titlepage)
            print("Videopage:", url_videopage)
            print("Chunk:", url_chunk)
            data['url_chunk'] = url_chunk
            data['content'] = "pbs_" + content
            print("\n"*5)
            
            with open("url_pbs_" + content + ".csv", 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                if csvfile.tell() == 0: # if csv file is empty
                    writer.writeheader()  # Write the header row
                writer.writerow(data)  # Write the data rows
            
            already_file = open("already_collected.txt", 'a')
            already_file.write(name+"\n")

    total_count = 0
    for content, count in count_dict.items():
        print(content, count)
        total_count += count


    print("TOTAL=", total_count)







