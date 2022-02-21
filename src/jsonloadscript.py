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


################ UTILITY FUNCTIONS ################

DYNMADO = 'https://apl.unob.cz/dymado/odata/'

def data(data):
    text = data
    return text


def loadJSONPage(link):
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        print(data)

async def Analyze(data):
    value = data["value"]
    result = {"kod" : [], "zkratka" : [], "rok_nast" : [], "generovany_nazev" : []}
    for item in enumerate(value):
        result["kod"].append(item["kod"])
        result["zkratka"].append(item["zkratka"])
        result["rok_nast"].append(item["rok_nast"])
        result["generovany_nazev"].append(item["generovany_nazev"])
    return result

async def saveJson(data):
    jsonData = Analyze(data)
    with open("outputs/jsondata.json", "w", encoding = "utf8") as f:
        json.dump(jsonData, f, indent=2)
    pass
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
            return document.querySelector("body").innerText
        }
    ''')

    Analyze(innerText)
    saveJson(Analyze(innerText))

    #loadJSONPage(DYNMADO + "Stud_skupiny")

    # await page.screenshot({'path': 'outputs/example.png'})

    #r = requests.get('https://apl.unob.cz/dymado/odata/Stud_skupiny')

    print(innerText)

    # print(r.json())

    await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())