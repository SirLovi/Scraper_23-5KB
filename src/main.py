import asyncio
from bs4 import BeautifulSoup
from pyppeteer import *
import os


################ MAIN ################

login_url = ('https://adfs.unob.cz/adfs/ls?version=1.0&action=signin&realm=urn%3AAppProxy%3Acom&appRealm=24ce5c4c-88e7-e611-80c1-005056864eb3&returnUrl=https%3A%2F%2Fintranet.unob.cz%2Fprehledy%2FStranky%2FStudenti.aspx&client-request-id=A62EBCC3-8ED1-0001-7D6A-DCAAD18ED701')
auth_url = ('https://adfs.unob.cz:443/adfs/ls?version=1.0&action=signin&realm=urn%3AAppProxy%3Acom&appRealm=24ce5c4c-88e7-e611-80c1-005056864eb3&returnUrl=https%3A%2F%2Fintranet.unob.cz%2Fprehledy%2FStranky%2FStudenti.aspx&client-request-id=A62EBCC3-8ED1-0001-C48B-DCAAD18ED701')

async def main():
    browser = await launch(headless=False, userDataDir='./userdata',args=['--disable-infobars'])
    page = await browser.newPage()
    await page.goto('https://intranet.unob.cz/prehledy/Stranky/Studenti.aspx')

    #await page.screenshot({'path': 'outputs/example.png'})

    await asyncio.sleep(100)
    
    
    #await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

