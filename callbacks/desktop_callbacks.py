from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format
import dash
import plotly.express as px
import json
import requests

import sys
sys.path.append('../')
from utils import StatesDataFrame, CountiesDataFrame, COORDS, cosine_sim, StateFlags
from components import existing_vs_new_chart, existing_vs_new_chart_counties, positive_pct_chart, choropleth_mapbox, choropleth_mapbox_counties, create_cards, daily_stats
from credentials.creds import AWS_SERVER_PUBLIC_KEY, AWS_SERVER_SECRET_KEY
import boto3
with open('web_scraping/states.json', 'r') as f:
    stateAbbrevs = json.load(f)
stateAbbrevs = {v: k for k,v in stateAbbrevs.items()}




def register_desktop_callbacks(app):

    
    ## create the flag based on which state_picker value has been chosen
    @app.callback(
        Output('flag', 'src'),
        [Input("state_picker", "value")])
    def get_flag(state):
        if state == 'United States' or state == 'U.S.':
            return 'https://www.nationsonline.org/flags_big/United_States_lgflag.gif'
        else:
            try:
                print(state)
                url = 'https://dynamic-covid19-analysis.s3.us-east-2.amazonaws.com/{}.png'.format(state)
                print(url.format(state))
                return url.format(state)
            except:
                return None

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

   