from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd 
from urllib.request import urlopen
import json

import sys
sys.path.append('../')
from utils import StatesDataFrame, COORDS

statesJSON = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json').json()




def choropleth_mapbox(state, period, df, lati, long, criteria):
    print(lati, long)
    # lati, long = 45.5017, -73.5673
    # df = pd.read_csv('todays_data.csv')
    if criteria == 'cases':
        mapDf = df[['state', 'date', 'new positive cases (last 7 days)']].fillna(0)
        mapDf['period'] = mapDf.groupby('state')['new positive cases (last 7 days)'].shift(period*7)
        mapLatest = mapDf[mapDf['date'] == mapDf['date'].max()]
        mapLatest['% Difference'] = ((mapLatest['new positive cases (last 7 days)'] - mapLatest['period'])/mapLatest['period'])*100
        mapLatest = mapLatest.fillna(0)
        mapLatest['% Difference'] = mapLatest['% Difference'].apply(lambda x: int(x))
    else:
        mapDf = df[['state', 'date', 'new deaths (last 7 days)']].fillna(0)
        mapDf['period'] = mapDf.groupby('state')['new deaths (last 7 days)'].shift(period*7)
        mapLatest = mapDf[mapDf['date'] == mapDf['date'].max()]
        mapLatest['% Difference'] = ((mapLatest['new deaths (last 7 days)'] - mapLatest['period'])/mapLatest['period'])*100
        mapLatest = mapLatest.fillna(0)
        mapLatest['% Difference'] = mapLatest['% Difference'].apply(lambda x: int(x))
    
    # template_new = "{locations}: %{customdata} change over the last {} weeks".format(period)
    if state == 'United States':
        fig = px.choropleth_mapbox(mapLatest,
            geojson = statesJSON,
            locations= 'state',
            color = '% Difference',
            color_continuous_scale='balance',
            opacity = 0.7,
            range_color = [-100, 100],
            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
            template="plotly_dark",
            mapbox_style = 'satellite-streets'
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox = dict(accesstoken='pk.eyJ1IjoicmVpZmZkIiwiYSI6ImNrOHFjaXlmOTAyaW0zamp6ZzI4NmtmMTQifQ.4EOhJ5NJJpawQnnoBXGCkw'))
    else:
        fig = px.choropleth_mapbox(mapLatest,
            geojson = statesJSON,
            locations= 'state',
            color = '% Difference',
            color_continuous_scale='balance',
            opacity = 0.7,
            range_color = [-100, 100],
            zoom=5, center = {"lat": COORDS[state]['lat'], "lon": COORDS[state]['long']},
            template="plotly_dark",
            mapbox_style = 'satellite-streets'
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox= dict(accesstoken = 'pk.eyJ1IjoicmVpZmZkIiwiYSI6ImNrOHFjaXlmOTAyaW0zamp6ZzI4NmtmMTQifQ.4EOhJ5NJJpawQnnoBXGCkw'))

    if lati != 0:
        fig.add_trace(go.Scattermapbox(
            lat=[lati],
            lon=[long],
            mode='markers+text',
            text=['My Current Location'],
            textposition = "bottom right",
            hoverinfo = 'none',
            marker=go.scattermapbox.Marker(
            size=12,
            color='rgb(238, 198, 67)',
            opacity=0.7
        )))
    return fig



def choropleth_mapbox_counties(state, period, df, lati, long, criteria):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    # df = pd.read_csv('utils/todays_county_data.csv')
    if criteria == 'cases':
        mapDf = df[['state', 'county', 'date', 'fips', 'new positive cases (last 7 days)']]
        print(mapDf)
        mapDf = mapDf[mapDf['state'] == state]
        print(mapDf)
        mapDf['period'] = mapDf.groupby('fips')['new positive cases (last 7 days)'].shift(period*7)
        mapLatest = mapDf[mapDf['date'] == mapDf['date'].max()]
        mapLatest['% Difference'] = ((mapLatest['new positive cases (last 7 days)'] - mapLatest['period'])/mapLatest['period'])*100
        mapLatest['fips'] = mapLatest['fips'].apply(lambda x: str(x).zfill(5))
        print(mapLatest)
    else:
        mapDf = df[['state', 'county', 'date', 'fips', 'new deaths (last 7 days)']]
        print(mapDf)
        mapDf = mapDf[mapDf['state'] == state]
        print(mapDf)
        mapDf['period'] = mapDf.groupby('fips')['new deaths (last 7 days)'].shift(period*7)
        mapLatest = mapDf[mapDf['date'] == mapDf['date'].max()]
        mapLatest['% Difference'] = ((mapLatest['new deaths (last 7 days)'] - mapLatest['period'])/mapLatest['period'])*100
        mapLatest['fips'] = mapLatest['fips'].apply(lambda x: str(x).zfill(5))
        print(mapLatest)


    fig = px.choropleth_mapbox(mapLatest,
        geojson=counties,
        locations='fips',
        color = '% Difference',
        color_continuous_scale='balance',
        opacity = 0.7,
        range_color = [-200, 200],
        hover_data = ['county', '% Difference'],
        zoom=5, center = {"lat": COORDS[state]['lat'], "lon": COORDS[state]['long']},
        template="plotly_dark",
        mapbox_style = 'satellite-streets' )
    if lati != 0:
        fig.add_trace(go.Scattermapbox(
            lat=[lati],
            lon=[long],
            mode='markers+text',
            text=['My Current Location'],
            textposition = "bottom right",
            hoverinfo = 'none',
            marker=go.scattermapbox.Marker(
            size=12,
            color='rgb(238, 198, 67)',
            opacity=0.7
        )))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox= dict(accesstoken = 'pk.eyJ1IjoicmVpZmZkIiwiYSI6ImNrOHFjaXlmOTAyaW0zamp6ZzI4NmtmMTQifQ.4EOhJ5NJJpawQnnoBXGCkw'))
    fig.update_layout(clickmode='event+select')
    return fig

