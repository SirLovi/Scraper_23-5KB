import asyncio
from bs4 import BeautifulSoup
from pyppeteer import *
import os
import json


################ UTILITY FUNCTIONS ################



################ MAIN ################

async def main():

    # RENAME "loginConfig_EXAMPLE.json" TO "loginConfig.json" FOR THE SCRIPT TO WORK CORRECTLY!!
    # "loginConfig.json" is ignored by GIT so your private login info is not shared
    # YOU DON'T WANT YOUR LOGIN INFO ON GITHUB!
    
    with open('src/loginConfig.json', 'r') as f:
        content = f.read()
        loginConfig = json.loads(content)


    browser = await launch(headless=False, userDataDir='./userdata',args=['--disable-infobars','--incognito'])
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()

    await page.goto('https://intranet.unob.cz/prehledy/Stranky/StudijniSkupiny.aspx')

    await page.type('[id=userNameInput]', loginConfig.get('username'))
    await page.type('[id=passwordInput]', loginConfig.get('password'))
    await page.keyboard.press('Enter')
    await page.waitForNavigation()

    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101010701')
    
    #await page.screenshot({'path': 'outputs/example.png'})
    
    await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())