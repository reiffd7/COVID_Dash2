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


def register_desktop_callbacks(app):
    df = StatesDataFrame().df
    df.to_csv('utils/todays_data.csv')

    county_df = CountiesDataFrame().df
    county_df.to_csv('utils/todays_county_data.csv')
    
    @app.callback(
        Output('flag', 'src'),
        [Input("state_picker", "value")])
    def get_flag(state):
        if state == 'United States' or state == 'U.S.':
            return 'https://www.nationsonline.org/flags_big/United_States_lgflag.gif'
        else:
            return StateFlags[state]

    @app.callback(
        Output('page-title', 'children'),
        [Input('state_picker', 'value')])
    def get_site_title(state):
        if state == 'United States':
            return 'United States COVID-19 Analysis'
        else:
            return '{} COVID-19 Analysis'.format(stateAbbrevs[state])


    @app.callback(
        Output('choropleth', 'clickData'),
        [Input('map-container', 'n_clicks')]
    )
    def reset_clickData(n_clicks):
        return None

    @app.callback(
        Output('state_picker', 'value'),
        [Input('choropleth', 'clickData')]
    )
    def update_states(clickData):
        if clickData == None:
            return dash.no_update
        else:
            try:
                test = int(clickData["points"][0]["location"])
                return dash.no_update
            except:
                state = clickData["points"][0]["location"]
                return state

    
    

    @app.callback(
        Output('slider-output', 'children'),
        [Input('period-slider', 'value')]
    )
    def get_slider_value(value):
        return '{} weeks'.format(value)

    @app.callback(
        Output('daily-stats', 'children'),
        [Input('state_picker', 'value'),
        Input('period-slider', 'value')]
    )
    def daily_stats_callback(state, period):
        return daily_stats(state, period)

    @app.callback(
    [Output("existing-vs-new-chart-title", "children")],
    [Input("state_picker", "value"),
    Input("period-slider", "value"),
    Input('choropleth', 'clickData')],
    )                                                   # pylint: disable=W0612
    def confirmed_cases_chart_title_callback(state, period, clickData):
        if state == "U.S.":
            return ["U.S. Last {} Weeks Cases vs. New Cases".format(period)]
        else:
            if clickData == None:
                return ["{} Last {} Weeks Cases vs. New Cases".format(state, period)]
            else:
                try:
                    county = clickData["points"][0]["customdata"][0]
                    return ["{} vs {} County, Last {} Weeks Cases vs. New Cases".format(state, county, period)]
                except:
                    state = clickData["points"][0]["location"]
                    return ["{} Last {} Weeks Cases vs. New Cases".format(state, period)]


    @app.callback(
        [Output("existing-vs-new", "figure")],
        [Input("state_picker", "value"),
        Input("period-slider", "value"),
        Input('choropleth', 'clickData')]
    )
    def existing_vs_new_chart_callback(state, period, clickData):
        if clickData == None:
            fig = existing_vs_new_chart(state, period)
            return [fig]
        else:
            try:
                county = clickData["points"][0]["customdata"][0]
                fig = existing_vs_new_chart_counties(state, county, period)
                return [fig]
            except:
                state = clickData["points"][0]["location"]
                fig = existing_vs_new_chart(state, period)
                return [fig]


    @app.callback(
    [Output("positive-pct-title", "children")],
    [Input("state_picker", "value"),
    Input("period-slider", "value")],
    )                                                   # pylint: disable=W0612
    def positive_pct_title_callback(state, period):
        if state == "U.S.":
            return ["U.S. Last {} Weeks Positive % vs. Last Week's Positive %".format(period)]

        return ["{} Last {} Weeks Positive % vs. Last Week's Positive %".format(state, period)]

    @app.callback(
        [Output("positive-pct", "figure")],
        [Input("state_picker", "value"),
        Input("period-slider", "value")]
    )
    def positive_pct_chart_callback(state, period):
        fig = positive_pct_chart(state, period)
        return [fig]

    @app.callback(
        Output('choropleth', 'figure'),
        [Input('state_picker', 'value'),
        Input('period-slider', 'value')])
    def map_content(state, period):
        if state == 'United States' or state == 'U.S.':
            return choropleth_mapbox(state, period)
        else:
            return choropleth_mapbox_counties(state, period)
            

    @app.callback(
        Output('sim-states', 'children'),
        [Input('state_picker', 'value'),
        Input('period-slider', 'value')]
    )
    def sim_states_callback(state, period):
        if state == 'United States' or state == 'U.S.':
            return None
        else:
            return create_cards(state, period)

    

    @app.callback(
        Output('click-data', 'children'),
        [Input('choropleth', 'clickData')]
    )
    def display_click_data(clickData):
        return json.dumps(clickData, indent=2)

    
     

        


