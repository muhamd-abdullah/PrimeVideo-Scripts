import asyncio
from pyppeteer import launch
import csv
import time
import os

profile_path = '/Users/abdullah/Library/Application Support/Google/Chrome/Default'
exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

async def get_url_of_vidchunk(url):
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    chunk_url = [""]

    def interception_fun(response):
        if (".m4s?" in response.url and "/video/" in response.url):
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
        #await page.goto(url, waitUntil='domcontentloaded')
        await page.goto(url)
        page.on('response', interception_fun)
        viewport_options = {'width': 1920, 'height': 1080}
        await page.setViewport(viewport_options)
        #await page.mouse.click(300,100)
        
        
        await asyncio.sleep(3)

        #focus_element = await page.waitForSelector('body')
        #await focus_element.click()

        # Click only buttons with text 'Watch'
        await page.evaluate('''async () => {
            const buttons = document.querySelectorAll('button');
            for (const button of buttons) {
                if (button.textContent.includes('Watch') && button.textContent.includes('Category')) {
                    button.click();
                    await new Promise(resolve => setTimeout(resolve, 100));  // Wait for 100 ms between clicks
                }
            }
        }''')

        start_time = time.time()
        elapsed_time = 0
        print("clicking on watch button")
        await page.mouse.click(50,590)
        #await asyncio.sleep(15)
        while True:
            if chunk_url[0] != "":
                break
            else:
                print("waiting for 1 more sec")
                await asyncio.sleep(1) # load page for 1 more sec
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 10: # max timeout in sec
                break

    except Exception as e:
        print(url,"\n",e)
    
    await browser.close()
    print(f"returning --> {chunk_url[0]}\n")
    return chunk_url[0]






url_videopage = "https://pluto.tv/en/on-demand/movies/a-kid-in-king-arthurs-court-1994-1-1/details"
url_chunk = asyncio.get_event_loop().run_until_complete(get_url_of_vidchunk(url_videopage))