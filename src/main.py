import asyncio
from bs4 import BeautifulSoup
from pyppeteer import *
import os
import json
import pandas as pd


################ UTILITY FUNCTIONS ################

URL = 'https://intranet.unob.cz/prehledy/Stranky/StudijniSkupiny.aspx'

async def get_page(browser, url, selector):
    """Return a page after waiting for the given selector"""
    page = await browser.newPage()
    await page.goto(url)
    await page.waitForSelector(selector)
    return page

async def get_urls(browser):
    """Return the total number of pages available"""
    page = await get_page(browser, URL.format(0), 'div.ms-Help-PanelContainer')
    urls = await page.evaluate('''
        () => {
            const links = document.querySelectorAll('ctl00_PlaceHolderMain_GridView1 a')
            const urls = Array.from(links).map(link => link.href)
            return urls
        }
    ''')

async def get_num_pages(browser):
    """Return the total number of pages available"""
    page = await get_page(browser, URL.format(0), 'div.ms-Help-PanelContainer')
    num_pages = await page.querySelectorEval(
        'div.ng-isolate-scope',
        '(element) => element.getAttribute("data-num-pages")')
    return int(num_pages)


async def get_table(browser, page_nb):
    """Return the table from the given page number as a pandas dataframe"""
    print(f'Get table from page {page_nb}')
    page = await get_page(browser, URL.format(page_nb), 'td.res-startNo')
    table = await page.querySelectorEval('table', '(element) => element.outerHTML')
    return pd.read_html(table)[0]


async def get_results():
    """Return all the results as a pandas dataframe"""
    browser = await launch()
    num_pages = await get_num_pages(browser)
    print(f'Number of pages: {num_pages}')
    # Python 3.6 asynchronous comprehensions! Nice!
    dfs = [await get_table(browser, page_nb) for page_nb in range(0, num_pages)]
    await browser.close()
    df = pd.concat(dfs, ignore_index=True)
    return df


################ MAIN ################

width, height = 1440, 900

async def main():

    # RENAME "loginConfig_EXAMPLE.json" TO "loginConfig.json" FOR THE SCRIPT TO WORK CORRECTLY!!
    # "loginConfig.json" is ignored by GIT so your private login info is not shared
    # YOU DON'T WANT YOUR LOGIN INFO ON GITHUB!

    with open('src/loginConfig_SECRET.json', 'r') as f:
        content = f.read()
        loginConfig = json.loads(content)


    browser = await launch(headless=False, userDataDir='./userdata',args=['--disable-infobars','--incognito',f'--window-size={width},{height}'])
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()

    await page.setViewport({'width': width, 'height': height})
    await page.goto('https://intranet.unob.cz/prehledy/Stranky/StudijniSkupiny.aspx')

    await page.type('[id=userNameInput]', loginConfig.get('username'))
    await page.type('[id=passwordInput]', loginConfig.get('password'))
    await page.keyboard.press('Enter')
    await page.waitForNavigation()
    
    urls = await page.evaluate('''
        () => {
            const links = document.querySelectorAll('ctl00_PlaceHolderMain_GridView1 a')
            const urls = Array.from(links).map(link => link.href)
            return urls
        }
    ''')
    
    print(urls)
    await page.goto(urls[0])
    """
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101010701')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101010703')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101011501')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101011601')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101011603')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101011701')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101011703')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101020701')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101020703')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101021501')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101021601')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101021701')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101021703')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101030701')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101030703')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101031501')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101031601')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101690701')
    await page.goto('https://intranet.unob.cz/prehledy/SitePages/stskupiny2.aspx?hr=9101690703')
    """
    
   
    
    await page.screenshot({'path': 'outputs/example.png'})
    
    await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())