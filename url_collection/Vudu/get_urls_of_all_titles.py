import asyncio
from pyppeteer import launch
import csv
import time
import os

'''
SIGN-IN ACCOUNT BEFOREHAND TO MAKE IT WORK!
example chunk urls:

(1)
https://ic-2d58de00-065aae-4vuduavod.s.loris.llnwd.net/225/3830331/dash/h264-2000.mp4/range/	
9383467-9618500?s=1691518735	<---- difference
&e=1691605735	
&u=87791344	
&p=46	
&h=32e441a228b4d51900c2ba3da6a4aa56

(2)
https://ic-2d58de00-065aae-4vuduavod.s.loris.llnwd.net/225/3830331/dash/h264-2000.mp4/range/
10840581-11084088?s=1691518735   <---- difference
&e=1691605735
&u=87791344
&p=46
&h=32e441a228b4d51900c2ba3da6a4aa56


Input: URL of the page containing list of all movies/tvs
Output: This returns individual URLs of the title page, videopage, and chunk of each movie/tv
'''

profile_path = '/Users/abdullah/Library/Application Support/Google/Chrome/Default'
exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

#urls_main_top = {
#'url_space' : 'https://www.magellantv.com/genres/space',
#}

urls_main_top = {
}


content_names = [] # store to avoid duplicate movie/tv titles


async def get_url_of_vidchunk(url):
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    chunk_url = [""]

    def interception_fun(response):
        if (".mp4" in response.url and "h264" in response.url):
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
        await page.goto(url, waitUntil='networkidle0')
        page.on('response', interception_fun)
        
        #await asyncio.sleep(60000) #### FOR SIGN-IN !!!!!

        await page.waitForSelector('body')

        # Click only buttons with text 'Watch'
        await page.evaluate('''async () => {
            const buttons = document.querySelectorAll('button');
            for (const button of buttons) {
                if (button.textContent.includes('Watch') || button.textContent.includes('Resume')) {
                    button.click();
                    await new Promise(resolve => setTimeout(resolve, 100));  // Wait for 100 ms between clicks
                }
            }
        }''')

        start_time = time.time()
        elapsed_time = 0
        while True:
            if chunk_url[0] != "":
                break
            else:
                print("waiting for 1 more sec")
                await asyncio.sleep(1) # load page for 1 more sec
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 60: # max timeout in sec
                break

    except Exception as e:
        print(url,"\n",e)
    
    await browser.close()
    print(f"returning --> {chunk_url[0]}\n")
    return chunk_url[0]



async def scroll_to_bottom(page):
    all_link_data = []
    counter = 0
    viewport_options = {'width': 1920, 'height': 1080}
    await page.setViewport(viewport_options)
    while True:
        print(f"Scrolling... ({counter+1})")
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
        
        previous_height = await page.evaluate('document.body.scrollHeight')
        await asyncio.sleep(1)  # Adjust the sleep time as needed
        current_height = await page.evaluate('document.body.scrollHeight')

        all_link_data.extend(link_data)
  
        if previous_height == current_height:
            pass
            #return all_link_data
        
        if counter == 5:
            return all_link_data
        
        counter += 1
    

async def get_link_addresses(url):
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    page = await browser.newPage()
    #await page.goto(url)
    await page.goto(url, waitUntil='networkidle0')
    
    all_link_data = await scroll_to_bottom(page)

    await browser.close()
    return all_link_data


async def get_all_links(url):
    all_link_data = await get_link_addresses(url)
    all_link_data_new = [] # removes duplicates, add videopage url
    global content_names

    for data in all_link_data:
        name = data['text']
        url_title = data['href']
        #print(data['href'],"\n\n")

        # for genres
        if "/uxrow/" in data['href']:
            print(data['href'])
            genre = data['href'].rsplit("/", 3)[-2]
            urls_main_top[genre] = url_title
        
        # for video links
        if "www.vudu.com/content/movies/details/" in data['href']:
            print(data['href'])
            url_videopage = url_title
            content_names.append(name)
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

    # fill genre urls
    _ = asyncio.get_event_loop().run_until_complete(get_all_links("https://www.vudu.com/content/movies/uxrow/Browse-All-Free-Titles/252"))
    print("Genre URLs:\n",len(urls_main_top),"\n",urls_main_top,"\n\n")
    #exit()

    genre_count = 0
    for content, main_url in urls_main_top.items():
        genre_count += 1
        print("\n"*10, "*"*25, f"{content} ({genre_count}/{len(urls_main_top)})", "*"*25, "\n\n")
        
        # get videopage links
        all_link_data_new = asyncio.get_event_loop().run_until_complete(get_all_links(main_url))
        count_dict[content] = len(all_link_data_new)
        print(f"{content} = {len(all_link_data_new)}")

        count = 0  
        print("\n\n")
        
        # play video in each link & get chunk url
        for data in all_link_data_new:
            count += 1
            name = data['url_titlepage'].rsplit("/", 1)[-1]
            data['name'] = name
            print(f"**** {count} out of {len(all_link_data_new)} --- {content} ({genre_count}/{len(urls_main_top)}) ~~~ elapsed: {elapsed_time} min ****")

            current_time = time.time()
            elapsed_time = int((current_time - start_time)//60)

            if name+"\n" in already_collected:
                print(f"{name} is already collected!\n\n\n\n\n\n")
                continue
            
            url_titlepage = data['url_titlepage']
            url_videopage = data['url_videopage']
            
            url_chunk = asyncio.get_event_loop().run_until_complete(get_url_of_vidchunk(url_videopage))
            if url_chunk == "":
                print(f"failed to get url_chunk of {name}\n")
            
            print("Name:", name)
            print("Titlepage:", url_titlepage)
            print("Videopage:", url_videopage)
            print("Chunk:", url_chunk)
            data['url_chunk'] = url_chunk
            data['content'] = "vudu_" + content
            print("\n"*5)
            
            with open("url_" + content + ".csv", 'a', newline='') as csvfile:
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







