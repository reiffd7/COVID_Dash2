from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format
import dash
import plotly.express as px
import dash_html_components as html 
import json
import requests
from flask import request
import urllib3.request
import geocoder

import sys
sys.path.append('../')
from utils import StatesDataFrame, CountiesDataFrame, COORDS, cosine_sim, StateFlags
from components import existing_vs_new_chart, existing_vs_new_chart_counties, positive_pct_chart, choropleth_mapbox, choropleth_mapbox_counties, create_cards, daily_stats

with open('web_scraping/states.json', 'r') as f:
    stateAbbrevs = json.load(f)
stateAbbrevs = {v: k for k,v in stateAbbrevs.items()}

try:
    IP = request.headers['X-Forwarded-For']
except:
    IP = 'Not Found'

print('IP')
    

try:
    url = 'http://ip-api.com/json/{}'.format(IP)
    r = requests.get(url).json()
except:
    r = "location not found"




def register_desktop_callbacks(app):

    
    ## create the flag based on which state_picker value has been chosen
    @app.callback(
        Output('flag', 'src'),
        [Input("state_picker", "value")])
    def get_flag(state):
        if state == 'United States' or state == 'U.S.':
            return 'https://www.nationsonline.org/flags_big/United_States_lgflag.gif'
        else:
            return StateFlags[state]

    ## set the title of the page
    @app.callback(
        Output('page-title', 'children'),
        [Input('state_picker', 'value')])
    def get_site_title(state):
        if state == 'United States':
            return 'United States COVID-19 Analysis'
        else:
            return '{} COVID-19 Analysis'.format(stateAbbrevs[state])

    
    
    ## set the slider output
    @app.callback(
        Output('slider-output', 'children'),
        [Input('period-slider', 'value')]
    )
    def get_slider_value(value):
        return '{} weeks'.format(value)

    ## get IP address
    @app.callback(
        Output('ip-data', 'children'),
        [Input('input-on-submit', 'n_clicks')]
    )
    def get_ip(n_clicks):
        if n_clicks == None:
            return n_clicks
        if n_clicks%2 == 1:
            return [IP, r]


   