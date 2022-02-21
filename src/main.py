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

DYNMADO = 'https://apl.unob.cz/dymado/odata'

URL_link = 'https://intranet.unob.cz/prehledy/Stranky/StudijniSkupiny.aspx'


async def html_analyze(patternList, pageContent):
    result = {}
    for pat in patternList:
        currentName = pat["name"]
        currentPattern = pat["pattern"]
        currentSaveMulti = pat["saveMulti"]
        currentValue = re.findall(currentPattern, pageContent)
        if (type(currentName) == type(['b'])):
            # defined multiplae names
            index = 0
            for name in currentName:
                result[name] = currentValue[index]
                index = index + 1
        else:
            # defined single name
            if len(currentValue) > 0:
                if currentSaveMulti:
                    currentValue = currentValue
                else:
                    currentValue = currentValue[0]
            else:
                currentValue = ""
            result[currentName] = currentValue
    return result


async def getPrograms(htmlCode):
    analyzer_desc = [
        {'name': 'uic', 'saveMulti': True,
            'pattern': r'Uic</label>[^<]+<div[^>]+>[^0-9]+([0-9]+)'},
    ]
    analyseResult = html_analyze(analyzer_desc, htmlCode)
    return analyseResult['uic']


async def cacheItInFile(filePrefix):
    def decorator(func):
        async def resultFunc(id, page):
            fileName = f'{filePrefix}_{str(id)}.html'
            my_file = Path(fileName)
            if my_file.is_file():
                with open(fileName, 'r', encoding='utf-8') as f:
                    pageData = f.read()
            else:
                pageData = await func(id, page)
                with open(fileName, 'w', encoding='utf-8') as f:
                    f.writelines(pageData)
            return pageData
        return resultFunc
    return decorator


@cacheItInFile(filePrefix='_json_page')
async def loadJSONPage(link):
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        print(data)


@cacheItInFile(filePrefix='_main')
async def getMainPage(id=0, page=None):
    await page.goto('https://intranet.unob.cz/prehledy/Stranky/StudijniSkupiny.aspx')
    content = await page.content()
    return content


@cacheItInFile(filePrefix='_program')
async def getProgramPage(id, page):
    fullUrl = f'https://apl.unob.cz/Akreditace2017/StudijniProgram/{id}'
    await page.goto(fullUrl)
    content = await page.content()
    return content


@cacheItInFile(filePrefix='_program_ramec')
async def getProgramRamecPage(id, page):
    fullUrl = f'https://apl.unob.cz/Akreditace2017/StudijniProgram/{id}/PredmetRamec'
    await page.goto(fullUrl)
    content = await page.content()
    return content


async def getPredmet(programId):
    @cacheItInFile(filePrefix=f'_predmet')
    async def getProgramPredmetPage(id, page):
        fullUrl = f'https://apl.unob.cz/Akreditace2017/StudijniProgram/{programId}/PredmetRamec/{id}'
        await page.goto(fullUrl)
        content = await page.content()
        return content
    return getProgramPredmetPage


async def getSemestr(programId, predmetId):
    @cacheItInFile(filePrefix='_semestrPredmetu')
    async def getSemestrPage(id, page):
        fullUrl = f'https://apl.unob.cz/Akreditace2017/StudijniProgram/{programId}/PredmetRamec/{predmetId}/Predmet/{id}/Tema'
        await page.goto(fullUrl)
        content = await page.content()
        return content
    return getSemestrPage


async def analyzeProgramPage(html):
    def createPattern(name):
        return f'for="{name}"[^>]*>[^<]*<[^>]*>[^<]*<[^>]*>([^<]+)'
    analyzer_desc = [
        {'name': 'Predmety', 'saveMulti': True,
            'pattern': '/Akreditace2017/StudijniProgram/[0-9]+/PredmetRamec/([0-9]+)'}
    ]
    analyseResult = html_analyze(analyzer_desc, html)

    return analyseResult['Predmety']


async def analyzeProgramPage2(html):
    def createPattern(name):
        return f'for="{name}"[^>]*>[^<]*<[^>]*>[^<]*<[^>]*>([^<]+)'
    analyzer_desc = [
        {'name': 'uic', 'saveMulti': False, 'pattern': createPattern('Uic')},
        {'name': 'Zkratka', 'saveMulti': False,
         'pattern': createPattern('Zkratka')},
        {'name': 'Garant', 'saveMulti': False,
         'pattern': createPattern('PredmetGarantList')},
        {'name': 'Zastupce', 'saveMulti': False,
         'pattern': createPattern('PredmetGarantZastupceList')},
        {'name': 'PlatnostAkreditaceNorm', 'saveMulti': False,
         'pattern': createPattern('PlatnostAkreditaceNorm')},

        {'name': 'InsertUpdateNorm', 'saveMulti': False,
         'pattern': createPattern('InsertUpdateNorm')},
        {'name': 'PublikovatOdDoNorm', 'saveMulti': False,
         'pattern': createPattern('PublikovatOdDoNorm')},
        {'name': 'UpdatedBy', 'saveMulti': False,
         'pattern': createPattern('UpdatedBy')},
        {'name': 'CProfilStudijniProgram', 'saveMulti': False,
         'pattern': createPattern('CProfilStudijniProgram')},
        {'name': 'KKOV', 'saveMulti': False, 'pattern': createPattern('KKOV')},

        {'name': 'CisloRozhodnutiNau', 'saveMulti': False,
         'pattern': createPattern('CisloRozhodnutiNau')},
        {'name': 'CJazykStudia', 'saveMulti': False,
         'pattern': createPattern('CJazykStudia')},
        {'name': 'DelkaStudiaNorm', 'saveMulti': False,
         'pattern': createPattern('DelkaStudiaNorm')},
        {'name': 'CUdelAkadTitul', 'saveMulti': False,
         'pattern': createPattern('CUdelAkadTitul')},
        {'name': 'CFormaStudia', 'saveMulti': False,
         'pattern': createPattern('CFormaStudia')},

        {'name': 'CTypStudijniProgram', 'saveMulti': False,
         'pattern': createPattern('CTypStudijniProgram')},
        {'name': 'IsZamekZmeny', 'saveMulti': False,
         'pattern': createPattern('IsZamekZmeny')},
        {'name': 'SchvalenoOrgan', 'saveMulti': False,
         'pattern': createPattern('SchvalenoOrgan')},
        {'name': 'SchvalenoDatumNorm', 'saveMulti': False,
         'pattern': createPattern('SchvalenoDatumNorm')},
        {'name': 'SpolupracujiciInstituce', 'saveMulti': False,
         'pattern': createPattern('SpolupracujiciInstituce')},
        {'name': 'CIscedF', 'saveMulti': False,
         'pattern': createPattern('CIscedF')},
        {'name': 'RelevantniVnitrniPredpisy', 'saveMulti': False,
         'pattern': createPattern('RelevantniVnitrniPredpisy')},
        {'name': 'Predmety', 'saveMulti': True,
         'pattern': '/Akreditace2017/StudijniProgram/[0-9]+/PredmetRamec/([0-9]+)'}
    ]
    analyseResult = html_analyze(analyzer_desc, html)

    return analyseResult


async def analyzePredmetPage(html):
    analyzer_desc = [
        {'name': 'Temata', 'saveMulti': True,
            'pattern': '/Akreditace2017/StudijniProgram/[0-9]+/PredmetRamec/[0-9]+/Predmet/([0-9]+)/Tema'}
    ]
    analyseResult = html_analyze(analyzer_desc, html)
    return analyseResult['Temata']


async def analyzePredmetPage2(html):
    def createPattern(name):
        return f'for="{name}"[^>]*>[^<]*<[^>]*>[^<]*<[^>]*>([^<]+)'

    def createPattern2(title):
        return f'title="([^>]+)">[^<]*<[^>]*>[^<]*[^>]*[^<]*?(?="{title}")'

    analyzer_desc = [
        {'name': 'Uic', 'saveMulti': False, 'pattern': createPattern('Uic')},
        {'name': 'Zkratka', 'saveMulti': False,
         'pattern': createPattern('Zkratka')},
        {'name': 'Zalozeno', 'saveMulti': False,
         'pattern': createPattern('Zalozeno')},
        {'name': 'Soucast', 'saveMulti': False,
         'pattern': createPattern('Soucast')},
        {'name': 'CJazykStudia', 'saveMulti': False,
         'pattern': createPattern('CJazykStudia')},
        {'name': 'Specializace', 'saveMulti': False,
         'pattern': createPattern('Specializace')},
        {'name': 'ProfilujiciZaklad', 'saveMulti': False,
         'pattern': createPattern('ProfilujiciZaklad')},
        {'name': 'TeoretickyProfilujiciZaklad', 'saveMulti': False,
         'pattern': createPattern('TeoretickyProfilujiciZaklad')},
        {'name': 'StatniZkouska', 'saveMulti': False,
         'pattern': createPattern('StatniZkouska')},
        {'name': 'MultiSemestralni', 'saveMulti': False,
         'pattern': createPattern('MultiSemestralni')},
        {'name': 'PredmetJineSkoly', 'saveMulti': False,
         'pattern': createPattern('PredmetJineSkoly')},
        {'name': 'UpdatedBy', 'saveMulti': False,
         'pattern': createPattern('UpdatedBy')},

        {'name': 'Garanti', 'saveMulti': True,
         'pattern': '([^"]+)">[^<]+<[^<]+<[^<]+<a class="btn btn-sm px-1 py-0 border-0 openModal" title="Vymazat garanta"'},
        {'name': 'GarantiIds', 'saveMulti': True,
         'pattern': '[^"\(]+(\([0-9]+\))">[^<]+<[^<]+<[^<]+<a class="btn btn-sm px-1 py-0 border-0 openModal" title="Vymazat garanta"'},
        {'name': 'GarantiZastupci', 'saveMulti': True,
         'pattern': '([^"]+)">[^<]+<[^<]+<[^<]+<a class="btn btn-sm px-1 py-0 border-0 openModal" title="Vymazat zástupce garanta"'},
        {'name': 'GarantiZastupciIds', 'saveMulti': True,
         'pattern': '[^"\(]+(\([0-9]+\))">[^<]+<[^<]+<[^<]+<a class="btn btn-sm px-1 py-0 border-0 openModal" title="Vymazat zástupce garanta"'},
        {'name': 'Vyucujici', 'saveMulti': True,
         'pattern': '<div class="col-1" title="([^"]+)'},
        {'name': 'VyucujiciIds', 'saveMulti': True,
         'pattern': '<div class="col-1" title="[^"\(]+\(([0-9]+)\)'},

        {'name': 'Semestry', 'saveMulti': True,
         'pattern': '/Akreditace2017/StudijniProgram/[0-9]+/PredmetRamec/[0-9]+/Predmet/([0-9]+)/Tema'}
    ]

    analyseResult = html_analyze(analyzer_desc, html)
    return analyseResult


async def generateJSON():
    result = {'programy': [], 'predmety': [], 'semestry': [], 'temata': []}
    programIds = getPrograms(await getMainPage(0, None))
    for programId in programIds:
        programJson = analyzeProgramPage2(await getProgramPage(programId, None))
        predmetyIds = analyzeProgramPage(await getProgramRamecPage(programId, None))
        programJson['Predmety'] = predmetyIds
        result['programy'].append(programJson)

        for predmetId in predmetyIds:
            predmetJson = analyzePredmetPage2(await getPredmet(programId)(predmetId, None))
            result['predmety'].append(predmetJson)
            for semestrId in predmetJson['Semestry']:
                await getSemestr(programId, predmetId)(semestrId, None)

    return result


async def saveJSON():
    jsonData = await generateJSON()
    with open('jsondata.json', 'w', encoding='utf-8') as f:
        json.dump(jsonData, f, indent=2)
    pass


async def get_page(browser, url, selector):
    """Return a page after waiting for the given selector"""
    page = await browser.newPage()
    await page.goto(url)
    await page.waitForSelector(selector)
    return page


async def get_urls(browser):
    """Return the total number of pages available"""
    page = await get_page(browser, URL_link.format(0), 'div.ms-Help-PanelContainer')
    urls = await page.evaluate('''
        () => {
            const links = document.querySelectorAll('ctl00_PlaceHolderMain_GridView1 a')
            const urls = Array.from(links).map(link => link.href)
            return urls
        }
    ''')


async def get_num_pages(browser):
    """Return the total number of pages available"""
    page = await get_page(browser, URL_link.format(0), 'div.ms-Help-PanelContainer')
    num_pages = await page.querySelectorEval(
        'div.ng-isolate-scope',
        '(element) => element.getAttribute("data-num-pages")')
    return int(num_pages)


async def get_table(browser, page_nb):
    """Return the table from the given page number as a pandas dataframe"""
    print(f'Get table from page {page_nb}')
    page = await get_page(browser, URL_link.format(page_nb), 'td.res-startNo')
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

    browser = await launch(headless=False, userDataDir='./userdata', args=['--disable-infobars', '--incognito', f'--window-size={width},{height}'])
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()

    await page.setViewport({'width': width, 'height': height})
    await page.goto('https://intranet.unob.cz/prehledy/Stranky/StudijniSkupiny.aspx')

    await page.type('[id=userNameInput]', loginConfig.get('username'))
    await page.type('[id=passwordInput]', loginConfig.get('password'))
    await page.keyboard.press('Enter')
    await page.waitForNavigation()

    programIds = getPrograms(await getMainPage(0, page))
    for programId in programIds:
        programPage = await getProgramPage(programId, page)
        predmetyIds = analyzeProgramPage(await getProgramRamecPage(programId, page))
        for predmetId in predmetyIds:
            temataIds = analyzePredmetPage(await getPredmet(programId)(predmetId, page))
            for temaId in temataIds:
                await getSemestr(programId, predmetId)(temaId, page)

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
    asyncio.get_event_loop().run_until_complete(saveJSON())
