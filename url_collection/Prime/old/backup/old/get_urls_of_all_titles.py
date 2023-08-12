import asyncio
from pyppeteer import launch

'''
Input: URL of the page containing list of all movies/tvs
Output: This returns individual URLs of the title pages of movies/tvs
'''

profile_path = '/Users/abdullah/Library/Application Support/Google/Chrome/Default'
exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# URL containing all movies/tv shows list
url = "https://www.primevideo.com/browse/ref=atv_ge_aga_c_vqhlwi_1_smr?serviceToken=eyJ0eXBlIjoicXVlcnkiLCJuYXYiOnRydWUsInBpIjoiZGVmYXVsdCIsInNlYyI6ImNlbnRlciIsInN0eXBlIjoic2VhcmNoIiwicXJ5IjoicF9uX2VudGl0eV90eXBlPU1vdmllJmZpZWxkLWdlbnJlLWJpbj1hdl9nZW5yZV9hY3Rpb24maW5kZXg9ZXUtYW1hem9uLXZpZGVvLWV1cm8mYWR1bHQtcHJvZHVjdD0wJmJxPShub3QgYXZfc2Vjb25kYXJ5X2dlbnJlOidhdl9zdWJnZW5yZV9pbnRlcm5hdGlvbmFsX2luZGlhJykmc2VhcmNoLWFsaWFzPWluc3RhbnQtdmlkZW8mcHZfb2ZmZXJzPUNIOkNIOnN2b2Q6cHJpbWU6dm9kOi0xNjg2Njk2MDAwOjE2ODY2OTYwMDAtJnFzLWF2X3JlcXVlc3RfdHlwZT00JnFzLWlzLXByaW1lLWN1c3RvbWVyPTIiLCJydCI6InZRSEx3aXNtciIsInR4dCI6IlByaW1lIG1vdmllcyIsIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6IjBhZjJmYTQ4LTM1MWUtNDlkMC1hODdiLTBmNmU1MTU0MmNkNjoxNjg2Njk2NTQ2MDAwIiwic3RyaWQiOiIxOjFQTUdSNDIxSDNOSzEjI01aUVdHWkxVTVZTRUdZTFNONTJYR1pMTSIsIm9yZXFrIjoiMTJ5OHhUelFqalBwZExhYzVvdU5PVU9jKzFzcElKSVV6Tm1GaHVwUERIVT0iLCJvcmVxa3YiOjF9&jic=8%7CEgRzdm9k"


async def scroll_to_bottom(page):
    while True:
        previous_height = await page.evaluate('document.body.scrollHeight')
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(1)  # Adjust the sleep time as needed
        current_height = await page.evaluate('document.body.scrollHeight')
        if previous_height == current_height:
            break


async def get_link_addresses():
    browser = await launch(userDataDir=profile_path, headless=False, executablePath= exec_path)
    page = await browser.newPage()
    await page.goto(url)
    
    await scroll_to_bottom(page)

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
    
    await browser.close()
    return link_data


async def main():
    link_addresses = await get_link_addresses()
    for data in link_addresses:
        print("Text:", data['text'])
        print("Address:", data['href'])
        print("\n")



asyncio.get_event_loop().run_until_complete(main())