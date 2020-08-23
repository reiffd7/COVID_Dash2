from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd 
from urllib.request import urlopen
import dash_bootstrap_components as dbc 
import dash_core_components as dcc       
import dash_html_components as html  
import json

import sys
sys.path.append('../')
from utils import StatesDataFrame, COORDS

statesJSON = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json').json()




def choropleth_mapbox_animate(state, period, df, criteria):
    if criteria == 'cases':
        mapDf = df[['state', 'date', 'new positive cases (last 7 days)']].fillna(0)
        mapDf['period'] = mapDf.groupby('state')['new positive cases (last 7 days)'].shift(period*7)
        # mapDf = mapDf[mapDf['date'] == mapDf['date'].max()]
        mapDf['% Difference'] = ((mapDf['new positive cases (last 7 days)'] - mapDf['period'])/mapDf['period'])*100
        mapDf = mapDf.fillna(0)
        # mapDf['% Difference'] = mapDf['% Difference'].apply(lambda x: int(x))
    else:
        mapDf = df[['state', 'date', 'new deaths (last 7 days)']].fillna(0)
        mapDf['period'] = mapDf.groupby('state')['new deaths (last 7 days)'].shift(period*7)
        # mapDf = mapDf[mapDf['date'] == mapDf['date'].max()]
        mapDf['% Difference'] = ((mapDf['new deaths (last 7 days)'] - mapDf['period'])/mapDf['period'])*100
        mapDf = mapDf.fillna(0)
        # mapDf['% Difference'] = mapDf['% Difference'].apply(lambda x: int(x))
    mapDf = mapDf[mapDf['date'] >= '2020-04-01']
    mapDf['date'] = mapDf['date'].astype(str)
    # template_new = "{locations}: %{customdata} change over the last {} weeks".format(period)
    if state == 'United States':
        fig = px.choropleth_mapbox(mapDf,
            geojson = statesJSON,
            locations= 'state',
            color = '% Difference',
            animation_frame = 'date',
            color_continuous_scale='balance',
            opacity = 0.7,
            range_color = [-100, 100],
            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
            template="plotly_dark",
            mapbox_style = 'satellite-streets'
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox = dict(accesstoken='pk.eyJ1IjoicmVpZmZkIiwiYSI6ImNrOHFjaXlmOTAyaW0zamp6ZzI4NmtmMTQifQ.4EOhJ5NJJpawQnnoBXGCkw'))
    else:
        fig = px.choropleth_mapbox(mapDf,
            geojson = statesJSON,
            locations= 'state',
            color = '% Difference',
            animation_frame = 'date',
            color_continuous_scale='balance',
            opacity = 0.7,
            range_color = [-100, 100],
            zoom=5, center = {"lat": COORDS[state]['lat'], "lon": COORDS[state]['long']},
            template="plotly_dark",
            mapbox_style = 'satellite-streets'
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox= dict(accesstoken = 'pk.eyJ1IjoicmVpZmZkIiwiYSI6ImNrOHFjaXlmOTAyaW0zamp6ZzI4NmtmMTQifQ.4EOhJ5NJJpawQnnoBXGCkw'))

    # if lati != 0:
    #     fig.add_trace(go.Scattermapbox(
    #         lat=[lati],
    #         lon=[long],
    #         mode='markers+text',
    #         text=['My Current Location'],
    #         textposition = "bottom right",
    #         hoverinfo = 'none',
    #         marker=go.scattermapbox.Marker(
    #         size=12,
    #         color='rgb(238, 198, 67)',
    #         opacity=0.7
    #     )))
    card = dbc.CardBody(
        [
            html.Div(
                dcc.Loading(
                dcc.Graph(
                    figure = fig,
                    style={"height": "40vh"},
                    clear_on_unhover=True
                ),),
                id="map-container",
            ),
        ]
    )
    
    return card



def choropleth_mapbox_counties_animate(state, period, df, criteria):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    # df = pd.read_csv('utils/todays_county_data.csv')
    if criteria == 'cases':
        mapDf = df[['state', 'county', 'date', 'fips', 'new positive cases (last 7 days)']]
        mapDf = mapDf[mapDf['state'] == state]
        mapDf['period'] = mapDf.groupby('fips')['new positive cases (last 7 days)'].shift(period*7)
        # mapDf = mapDf[mapDf['date'] == mapDf['date'].max()]
        mapDf['% Difference'] = ((mapDf['new positive cases (last 7 days)'] - mapDf['period'])/mapDf['period'])*100
        mapDf['fips'] = mapDf['fips'].apply(lambda x: str(x).zfill(5))
        
    else:
        mapDf = df[['state', 'county', 'date', 'fips', 'new deaths (last 7 days)']]
        mapDf = mapDf[mapDf['state'] == state]
        mapDf['period'] = mapDf.groupby('fips')['new deaths (last 7 days)'].shift(period*7)
        # mapDf = mapDf[mapDf['date'] == mapDf['date'].max()]
        mapDf['% Difference'] = ((mapDf['new deaths (last 7 days)'] - mapDf['period'])/mapDf['period'])*100
        mapDf['fips'] = mapDf['fips'].apply(lambda x: str(x).zfill(5))

    mapDf['date'] = mapDf['date'].astype(str)
    print(mapDf['date'])
    fig = px.choropleth_mapbox(mapDf,
        geojson=counties,
        locations='fips',
        color = '% Difference',
        animation_frame = 'date',
        color_continuous_scale='balance',
        opacity = 0.7,
        range_color = [-200, 200],
        hover_data = ['county', '% Difference'],
        zoom=5, center = {"lat": COORDS[state]['lat'], "lon": COORDS[state]['long']},
        template="plotly_dark",
        mapbox_style = 'satellite-streets' )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox= dict(accesstoken = 'pk.eyJ1IjoicmVpZmZkIiwiYSI6ImNrOHFjaXlmOTAyaW0zamp6ZzI4NmtmMTQifQ.4EOhJ5NJJpawQnnoBXGCkw'))
    fig.update_layout(clickmode='event+select')
    return fig

