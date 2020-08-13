from dash.dependencies import Input, Output
import dash_table
from dash_table.Format import Format
import dash
import plotly.express as px
import json
import dash_html_components as html  
import requests
from flask import request
import sys
sys.path.append('../')
from utils import StatesDataFrame, CountiesDataFrame, COORDS, cosine_sim, StateFlags
from components import existing_vs_new_chart, existing_vs_new_chart_counties, positive_pct_chart, choropleth_mapbox, choropleth_mapbox_counties, create_cards, daily_stats

with open('web_scraping/states.json', 'r') as f:
    stateAbbrevs = json.load(f)
stateAbbrevs = {v: k for k,v in stateAbbrevs.items()}


def register_desktop_callacks_data(app):
    ## Load latest state & county data 

    dfOBJ = StatesDataFrame()
    df = dfOBJ.df
    # df = df[df['date'] >= '2020-04-20']
    # states = dfOBJ.states
    # df.to_csv('utils/todays_data.csv', index=False)
    
    county_dfOBJ = CountiesDataFrame()
    county_df = county_dfOBJ.df
    # county_df = county_df[county_df['date'] >= '2020-04-20']
    # county_df.to_csv('utils/todays_county_data.csv', index=False)


    ## positive-pct-chart title
    @app.callback(
        [Output("pospct_title", "children")],
        [Input("state_picker", "value"),
        Input('period-slider', 'value'),
        Input("choropleth", "hoverData"),
        Input("map-criteria", "value")]
    )                                                   # pylint: disable=W0612
    def positive_pct_title_callback(state, period, hoverData, criteria):
        print('shabba')
        if criteria == 'cases':
            title = 'Positive %'
        else:
            title = 'Death Rate'
        try:
            county = hoverData["points"][0]["customdata"][0]
            return ["{}: {} Over Time".format(state, title)]
        except:
            try:
                state = hoverData["points"][0]["location"]
                return ["{}: {} Over Time".format(state, title)]
            except:
                return ["{}: {} Over Time".format(state, title)]


    ## positive-pct-chart
    @app.callback(
        [Output("pospct_chart", "figure")],
        [Input("state_picker", "value"),
        Input('period-slider', 'value'),
        Input("choropleth", "hoverData"),
        Input("map-criteria", "value")]
    )
    def positive_pct_chart_callback(state, period, hoverData, criteria):
        try:
            county = hoverData["points"][0]["customdata"][0]
            return dash.no_update
        except:
            try:
                state = hoverData["points"][0]["location"]
                return [positive_pct_chart(state, df, criteria)]
            except:
                return [positive_pct_chart(state, df, criteria)]


    ## set the KPIs based on state_picker and period-slider
    @app.callback(
        Output('daily-stats', 'children'),
        [Input('state_picker', 'value'),
        Input('period-slider', 'value'),
        Input('choropleth', 'hoverData')]
    )
    def daily_stats_callback(state, period, hoverData):
        original_state = state
        try:
            county = hoverData["points"][0]["customdata"][0]
            return daily_stats(county, state, period, df, county_df)
        except:
            try:
                county = None
                state = hoverData["points"][0]["location"]
                if state in states:
                    return daily_stats(county, state, period, df, county_df)
            except:
                county = None
                return daily_stats(county, original_state, period, df, county_df)
            

    ## existing-vs-new-chart title
    @app.callback(
    [Output("existing-vs-new-chart-title", "children")],
    [Input("state_picker", "value"),
    Input("period-slider", "value"),
    Input("choropleth", "hoverData")],
    )                                                   # pylint: disable=W0612
    def confirmed_cases_chart_title_callback(state, period, hoverData):
        try:
            county = hoverData["points"][0]["customdata"][0]
            return ["{} vs {}: Last {} Weeks Cases vs. New Cases".format(state, county, period)]
        except:
            try:
                state = hoverData["points"][0]["location"]
                return ["{}: Last {} Weeks Cases vs. New Cases".format(state, period)]
            except:
                return ["{}: Last {} Weeks Cases vs. New Cases".format(state, period)]
            

    @app.callback(
        [Output("existing-vs-new", "figure")],
        [Input("state_picker", "value"),
        Input("period-slider", "value"),
        Input("choropleth", "hoverData")]
    )
    def existing_vs_new_chart_callback(state, period, hoverData):
        # if state == 'United States':
        #     return [existing_vs_new_chart(state, period)]
        try:
            county = hoverData["points"][0]["customdata"][0]
            fig = existing_vs_new_chart_counties(state, county, period, county_df, df)
            return [fig]
        except:
            try:
                state = hoverData["points"][0]["location"]
                fig = existing_vs_new_chart(state, period, df)
                return [fig]
            except:
                return [existing_vs_new_chart(state, period, df)]


    ## choropleth map based if a state has been picked or the US
    @app.callback(
        Output('choropleth', 'figure'),
        [Input('state_picker', 'value'),
        Input('period-slider', 'value'),
        Input('input-on-submit', 'n_clicks'),
        Input('map-criteria', 'value')])
    def map_content(state, period, n_clicks, criteria):
        lat, long = 0, 0
        if n_clicks == None:
            if state == 'United States' or state == 'U.S.':
                return choropleth_mapbox(state, period, df, lat, long, criteria)
            else:
                return choropleth_mapbox_counties(state, period, county_df, lat, long, criteria)
        if n_clicks%2 == 1:
            try:
                IP = request.headers['X-Forwarded-For'] 
            except:
                IP = 'Not Found'

            print(IP)
            try:
                url = 'http://ip-api.com/json/{}'.format(IP)
                rop = requests.get(url).json()
                lat, long = rop['lat'], rop['lon']
            except:
                rop = "location not found"
            if state == 'United States' or state == 'U.S.':
                return choropleth_mapbox(state, period, df, lat, long, criteria)
            else:
                return choropleth_mapbox_counties(state, period, county_df, lat, long, criteria)
        else:
            if state == 'United States' or state == 'U.S.':
                return choropleth_mapbox(state, period, df, lat, long, criteria)
            else:
                return choropleth_mapbox_counties(state, period, county_df, lat, long, criteria)
            
            



    ## similar state cards
    @app.callback(
        Output('sim-states', 'children'),
        [Input('state_picker', 'value'),
        Input('period-slider', 'value'),
        Input('sim-state-criteria', 'value')]
    )
    def sim_states_callback(state, period, criterias):
        if state == 'United States' or state == 'U.S.':
            return html.Div('Select a state to view the 5 most similar states based on metrics selected directly above')
        else:
            return create_cards(state, period, df, criterias)