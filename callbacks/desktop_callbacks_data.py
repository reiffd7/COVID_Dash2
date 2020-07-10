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

with open('web_scraping/states.json', 'r') as f:
    stateAbbrevs = json.load(f)
stateAbbrevs = {v: k for k,v in stateAbbrevs.items()}


def register_desktop_callacks_data(app):
    ## Load latest state & county data 

    dfOBJ = StatesDataFrame()
    df = dfOBJ.df
    # df = df[df['date'] >= '2020-04-20']
    states = dfOBJ.states
    df.to_csv('utils/todays_data.csv', index=False)
    
    county_dfOBJ = CountiesDataFrame()
    county_df = county_dfOBJ.df
    # county_df = county_df[county_df['date'] >= '2020-04-20']
    county_df.to_csv('utils/todays_county_data.csv', index=False)


    ## positive-pct-chart title
    @app.callback(
        [Output("pospct_title", "children")],
        [Input("state_picker", "value"),
        Input('period-slider', 'value'),
        Input("choropleth", "hoverData")]
    )                                                   # pylint: disable=W0612
    def positive_pct_title_callback(state, period, hoverData):
        print('shabba')
        try:
            county = hoverData["points"][0]["customdata"][0]
            return ["{}: Positive % Over Time".format(state)]
        except:
            try:
                state = hoverData["points"][0]["location"]
                return ["{}: Positive % Over Time".format(state)]
            except:
                return ["{}: Positive % Over Time".format(state)]


    ## positive-pct-chart
    @app.callback(
        [Output("pospct_chart", "figure")],
        [Input("state_picker", "value"),
        Input('period-slider', 'value'),
        Input("choropleth", "hoverData")]
    )
    def positive_pct_chart_callback(state, period, hoverData):
        try:
            county = hoverData["points"][0]["customdata"][0]
            return [positive_pct_chart(state, df)]
        except:
            try:
                state = hoverData["points"][0]["location"]
                return [positive_pct_chart(state, df)]
            except:
                return [positive_pct_chart(state, df)]


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
            
            state = hoverData["points"][0]["location"]
            if state in states:
                return daily_stats(state, period, df)
            else:
                return daily_stats(original_state, period, df)
            
        except:
            return daily_stats(original_state, period, df)


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
        Input('period-slider', 'value')])
    def map_content(state, period):
        if state == 'United States' or state == 'U.S.':
            return choropleth_mapbox(state, period, df)
        else:
            return choropleth_mapbox_counties(state, period, county_df)



    ## similar state cards
    @app.callback(
        Output('sim-states', 'children'),
        [Input('state_picker', 'value'),
        Input('period-slider', 'value')]
    )
    def sim_states_callback(state, period):
        if state == 'United States' or state == 'U.S.':
            return None
        else:
            return create_cards(state, period, df)