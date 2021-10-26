import asyncio
from bs4 import BeautifulSoup
from pyppeteer import *
import os


################ MAIN ################

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://intranet.unob.cz/prehledy/Stranky/Studenti.aspx')
    await page.screenshot({'path': 'outputs/example.png'})
    await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())