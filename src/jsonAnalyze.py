from encodings import utf_8
import json
from pyppeteer import *
import asyncio

async def data(data=[]):
    return data

async def Analyze(data):
    value = data["value"]
    result = {"kod" : [], "zkratka" : [], "rok_nast" : [], "generovany_nazev" : []}
    for index, item in enumerate(value):
        result["kod"].append(item["kod"])
        result["zkratka"].append(item["zkratka"])
        result["rok_nast"].append(item["rok_nast"])
        result["generovany_nazev"].append(item["generovany_nazev"])
    return result

async def saveJson(data):
    jsonData = await Analyze(data)
    with open("jsondata.json", "w", encoding = "utf-8") as f:
        json.dump(jsonData, f, indent=2)
    pass

async def main():
    with open('outputs/outputRaw.json', encoding = "utf-8") as f:
        data = json.load(f)
    data(data)
    
    Analyze(data)
    saveJson(data)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_until_complete(saveJson(data))