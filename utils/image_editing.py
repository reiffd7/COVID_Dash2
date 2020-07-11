from PIL import Image
import requests
from io import BytesIO
import numpy as np
import json




with open('../web_scraping/states.json', 'r') as f:
    states = json.load(f)
stateAbbrevs = {v: k for k,v in states.items()}

StateFlags = {k: 'https://geology.com/state-map/maps/{}-county-map.gif'.format(v.replace(' ', '-').lower()) for k,v in stateAbbrevs.items()}
urls = list(StateFlags.values())

for key, value in StateFlags.items():
    print(key)
    response = requests.get(value)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        img = img.convert('RGB')
        newData = []
        newData = []
        datas = img.getdata()

        for item in datas:
            if (item[2] == 255):
                newData.append((50, 56, 62))
            else:
                newData.append(item)
        img.putdata(newData)
        img.save("state_imgs/{}.png".format(key))