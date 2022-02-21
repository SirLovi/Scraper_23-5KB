import json

with open('outputs/outputRaw.json', encoding = "utf8") as f:
    data = json.load(f)

value = data["value"]
for index, item in enumerate(value):
    print(item["kod"])
    print(item["zkratka"])