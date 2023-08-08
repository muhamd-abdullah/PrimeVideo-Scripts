import asyncio
from pyppeteer import launch


profile_path = '/Users/abdullah/Library/Application Support/Google/Chrome/Default'
exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


async def click_watch_buttons(url):
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)

    try:
        page = await browser.newPage()
        await page.goto(url)
        
        # Wait for the page to load completely
        await page.waitForSelector('body')

        # Click only buttons with text "Watch"
        await page.evaluate('''async () => {
            const buttons = document.querySelectorAll('button');
            for (const button of buttons) {
                if (button.textContent.includes('Watch')) {
                    button.click();
                    await new Promise(resolve => setTimeout(resolve, 1000));  // Wait for 1 second between clicks
                }
            }
        }''')

        # Wait for a while to observe the clicks (you can adjust this time)
        await asyncio.sleep(5)

    except Exception as e:
        print("Error:", e)
    finally:
        await browser.close()

# Call the function with the target URL
target_url = "https://www.magellantv.com/video/zero-gravity-life-on-the-international-space-station?type=v"
asyncio.get_event_loop().run_until_complete(click_watch_buttons(target_url))
