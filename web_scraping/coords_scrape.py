import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np 
import json

with open('states.json', 'r') as f:
    states = json.load(f)


if __name__ == '__main__':
    url = 'https://inkplant.com/code/state-latitudes-longitudes'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", {"class":"table table-hover"})
    rows = table.find_all('tr')
    data = {}
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        entry = {}
        try:
            state = states[cols[0]]
            data[state] = {}
            data[state]['lat'] = float(cols[1])
            data[state]['long'] = float(cols[2])
            # data.append(entry)
        except:
            continue
    with open('coords.json', 'w') as f:
        json.dump(data, f)
  