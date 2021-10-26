import asyncio
from bs4 import BeautifulSoup
from pyppeteer import *
import os
import json


################ UTILITY FUNCTIONS ################



################ MAIN ################

async def main():

    with open('src/loginConfig.json', 'r') as f: # open the file in `path` for reading
        content = f.read()
        loginConfig = json.loads(content) # read the file as a dictionary into the config variable


    browser = await launch(headless=True, userDataDir='./userdata',args=['--disable-infobars'])
    page = await browser.newPage()
    await page.goto('https://intranet.unob.cz/prehledy/Stranky/StudijniSkupiny.aspx')
    await page.type('[id=userNameInput]', loginConfig.username)
    await page.type('[id=passwordInput]', loginConfig.password)
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101010701')
    await page.screenshot({'path': 'outputs/example.png'})
    
    await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())