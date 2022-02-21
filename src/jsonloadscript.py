import asyncio
from bs4 import BeautifulSoup
from pyppeteer import *
import os
import json
import pandas as pd
from pathlib import Path
import re
import urllib.request
import requests
import objectpath
from jsonAnalyze import Analyze


################ UTILITY FUNCTIONS ################

DYNMADO = 'https://apl.unob.cz/dymado/odata/'


def loadJSONPage(link):
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        json.dumps(data)


################ MAIN ################

width, height = 1440, 900


async def main():

    # RENAME "loginConfig_EXAMPLE.json" TO "loginConfig_SECRET.json" FOR THE SCRIPT TO WORK CORRECTLY!!
    # "loginConfig_SECRET.json" is ignored by GIT so your private login info is not shared
    # YOU DON'T WANT YOUR LOGIN INFO ON GITHUB!

    with open('src/loginConfig_SECRET.json', 'r') as f:
        content = f.read()
        loginConfig = json.loads(content)

    """
    browser = await launch(headless=False, userDataDir='./userdata', args=['--disable-infobars', '--incognito', f'--window-size={width},{height}'])
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    """

    browser = await launch(headless=False, userDataDir='./userdata', args=['--disable-infobars', f'--window-size={width},{height}'])
    page = await browser.newPage()

    await page.setViewport({'width': width, 'height': height})
    await page.goto(DYNMADO + "Stud_skupiny")

    await page.type('[id=Username]', loginConfig.get('username'))
    await page.type('[id=Password]', loginConfig.get('password'))
    await page.keyboard.press('Enter')

    await page.waitForNavigation()
    await page.waitForNavigation()

    # innerText = await page.content()

    innerText = await page.evaluate('''() =>  {
            return document.querySelector("value").innerText
        }
    ''')

    #loadJSONPage(DYNMADO + "Stud_skupiny")

    # await page.screenshot({'path': 'outputs/example.png'})

    #r = requests.get('https://apl.unob.cz/dymado/odata/Stud_skupiny')
    
    
    with open('outputs/outputRaw.json', 'w') as outfile:
        outfile.write(innerText)

    json.dump(Analyze(outfile))
    """
    print(outfile[0])
    # print(r.json())
    
    with open('outputs/outputRaw.json', 'r') as f:
        content = json.loads(f)
        keyval = 5
        if keyval in content:
            with open('outputs/test.json', 'w') as outfile:
                outfile.write(content[keyval])
    """
    await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
