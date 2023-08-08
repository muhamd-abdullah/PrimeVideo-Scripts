import asyncio
from pyppeteer import launch
import csv
import time
import os


with open("webpage_urls.txt", 'w') as myfile:
    print("new file created")



def write_dict_to_csv(filename, data_dict):
    fieldnames = list(data_dict.keys())
    file_exists = False
    
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            if fieldnames == reader.fieldnames:
                file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data_dict)



urls_mozilla = []


def get_resource_type(url):
    try:
        file_extension = os.path.splitext(url)[1]
        resource_type = file_extension[1:]  # Remove the dot from the extension
        if len(resource_type) == 3:
            if url not in urls_mozilla:
                urls_mozilla.append(url)
                data = {'name': url, 'url_chunk': url, 'content': 'mozilla'}
                write_dict_to_csv('mozilla_urls.csv', data)
                with open("webpage_urls.txt", 'a') as myfile:
                    myfile.write(url+"\n")
                return resource_type
            
        else:
            return "other"
    except:
        return None

elements_urls = []

profile_path = '/Users/abdullah/Library/Application Support/Google/Chrome/Default'
exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

content_names = [] # store to avoid duplicate movie/tv titles


async def get_url_of_vidchunk(url):
    browser = await launch(userDataDir=profile_path, headless=True, executablePath= exec_path)
    chunk_url = [""]

    def interception_fun(response):
        if str(response.url).endswith("js"):
            # Response logic goes here
            #print("URL:", response.url, "\n\n")
            chunk_url[0] = response.url
            chunk_url.append(response.url)
            print(chunk_url[-1])
            #print("Method:", response.request.method)
            #print("Response headers:", response.headers)
            #print("Request Headers:", response.request.headers)
            #print("Response status:", response.status)
        return
    
    try:
        page = await browser.newPage()
        await page.goto(url)
        page.on('response', interception_fun)
        
        # Trigger video playback using JavaScript
        await page.evaluate('''() => {
            const video = document.querySelector('video');
            if (video) {
                video.play();
            }
        }''')
        
        start_time = time.time()
        elapsed_time = 0 
        while True:
            if chunk_url[0] != "":
                break
            else:
                await page.waitFor(1000) # load page for 1 more sec
            
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 2: # max timeout
                break
    except Exception as e:
        print(url,"\n",e)
    
    await browser.close()
    return chunk_url


#url_videopage = "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Forwarded"
#url_videopage = "https://developer.mozilla.org"
url_videopage = "https://developer.mozilla.org/en-US/blog/"
#url_chunk = asyncio.get_event_loop().run_until_complete(get_url_of_vidchunk(url_videopage))






content_names = [] # store to avoid duplicate movie/tv titles


async def scroll_to_bottom(page):
    all_link_data = []
    start_time = time.time()
    elapsed_time = 0 
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
        
        previous_height = await page.evaluate('document.body.scrollHeight')
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        #await asyncio.sleep(1)  # Adjust the sleep time as needed
        current_height = await page.evaluate('document.body.scrollHeight')

        all_link_data.extend(link_data)
  
        if previous_height == current_height:
            return all_link_data
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > 2:
            break
    

async def get_link_addresses(url):
    browser = await launch(userDataDir=profile_path, headless=True, executablePath= exec_path)
    page = await browser.newPage()
    await page.goto(url)
    
    all_link_data = await scroll_to_bottom(page)

    await browser.close()
    return all_link_data


async def get_all_links(url):
    all_link_data = await get_link_addresses(url)
    all_link_data_new = [] # removes duplicates, add videopage url
    global content_names

    for data in all_link_data:
        if 'href' in data:
            url_title = data['href']
            url = url_title
            resource_type = get_resource_type(url)
            if resource_type and "other" not in resource_type:
                elements_urls.append(url)
                print(resource_type)
                continue
            name = data['text']
            #print(f"Name: {name}\nURL: {url_title}\n\n")
            content_names.append(name)
            data_new = {'name':name, 'url_titlepage':url_title}
            all_link_data_new.append(data_new)
            
    return all_link_data_new








all_link_data_new = asyncio.get_event_loop().run_until_complete(get_all_links(url_videopage))

i = 0
for data in all_link_data_new:
    try:
        url = data['url_titlepage']
        resource_type = get_resource_type(url)
        if resource_type and "other" not in resource_type:
            elements_urls.append(url)
            print(resource_type)
            continue
        print("\n"*5, i, url,"\n"*5)
        url_chunk = asyncio.get_event_loop().run_until_complete(get_all_links(url))
        for x in url_chunk:
            resource_type = get_resource_type(url)
            if resource_type:
                elements_urls.append(x)
        i += 1
    except:
        continue
    if i > 1000:
        break