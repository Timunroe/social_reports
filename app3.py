import asyncio
from pyppeteer import launch


async def main():
    # https://ca.linkedin.com/company/the-hamilton-spectator
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.thespec.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())