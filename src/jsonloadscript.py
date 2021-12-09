import asyncio
from bs4 import BeautifulSoup
from pyppeteer import *
import os
import json
import pandas as pd
from pathlib import Path
import re
import urllib.request


################ UTILITY FUNCTIONS ################

DYNMADO = 'https://apl.unob.cz/dymado/odata/'


async def loadJSONPage(link):
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        print(data)


################ MAIN ################

width, height = 1440, 900


async def main():

    # RENAME "loginConfig_EXAMPLE.json" TO "loginConfig_SECRET.json" FOR THE SCRIPT TO WORK CORRECTLY!!
    # "loginConfig_SECRET.json" is ignored by GIT so your private login info is not shared
    # YOU DON'T WANT YOUR LOGIN INFO ON GITHUB!

    with open('src/loginConfig_SECRET.json', 'r') as f:
        content = f.read()
        loginConfig = json.loads(content)

    browser = await launch(headless=False, userDataDir='./userdata', args=['--disable-infobars', '--incognito', f'--window-size={width},{height}'])
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()

    await page.setViewport({'width': width, 'height': height})
    # await page.goto(DYNMADO)
    await page.goto('https://intranet.unob.cz/prehledy/Stranky/StudijniSkupiny.aspx')

    await page.type('[id=userNameInput]', loginConfig.get('username'))
    await page.type('[id=passwordInput]', loginConfig.get('password'))
    await page.keyboard.press('Enter')
    await page.waitForNavigation()

    await loadJSONPage(DYNMADO + "Stud_skupiny")

    await page.screenshot({'path': 'outputs/example.png'})

    await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
