import asyncio
from pyppeteer import launch


profile_path = '/Users/abdullah/Library/Application Support/Google/Chrome/Default'
exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


async def get_url_of_vidchunk(url):
    browser = await launch(userDataDir=profile_path, headless=False, executablePath=exec_path)
    chunk_url = [""]

    def interception_fun(response):
        if (".m4s?" in response.url and "/video/" in response.url):
            print("URL:", response.url, "\n")
            chunk_url[0] = response.url
        return
    
    try:
        page = await browser.newPage()
        await page.goto(url)
        page.on('response', interception_fun)
        viewport_options = {'width': 1920, 'height': 1080}
        await page.setViewport(viewport_options)
        await asyncio.sleep(3)

        buttons = await page.querySelectorAll('button')
        for button in buttons:
            button_text = await page.evaluate('(element) => element.textContent', button)
            button_details = await button.boundingBox()
            print("Button Text:", button_text)
            print("Button Details:", button_details)
            print("-" * 40)

    except Exception as e:
        print("Error:", e)
    finally:
        await browser.close()




url_videopage = "https://pluto.tv/en/on-demand/movies/a-kid-in-king-arthurs-court-1994-1-1/details"
url_chunk = asyncio.get_event_loop().run_until_complete(get_url_of_vidchunk(url_videopage))