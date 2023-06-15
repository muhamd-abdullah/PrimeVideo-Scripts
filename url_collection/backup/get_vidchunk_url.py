import asyncio
import json
from pyppeteer import launch
profile_path = '/Users/abdullah/Library/Application Support/Google/Chrome/Default'
exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

'''
Input: URL of the webpage that plays the video
Output: This returns url of the HTTP video chunks response
'''


def interception_fun(response):
    if "_video_" in response.url and ".mp4" in response.url:
        # Response logic goes here
        print("URL:", response.url, "\n\n")
        #print("Method:", response.request.method)
        #print("Response headers:", response.headers)
        #print("Request Headers:", response.request.headers)
        #print("Response status:", response.status)
        return
    else:
        return


async def hmm():
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    page = await browser.newPage()
    await page.goto('https://www.primevideo.com/detail/0SK5HM5PYJC9H4FUBRLNJSHKHQ/ref=atv_hm_fcv_prime_sd_mv_resume_t1ACAAAAAA0wh0?autoplay=1&t=0')
    page.on('response', interception_fun)
    # Trigger video playback using JavaScript
    await page.evaluate('''() => {
        const video = document.querySelector('video');
        if (video) {
            video.play();
        }
    }''')

    video_duration = 5 #seconds
    # Wait for the video to play for the specified duration
    await page.waitFor(video_duration * 1000)  # Convert seconds to milliseconds

    
    
    await browser.close()

    return

asyncio.get_event_loop().run_until_complete(hmm())


