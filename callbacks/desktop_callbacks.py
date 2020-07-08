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

    ## Load latest state and county data
    
    dfOBJ = StatesDataFrame()
    df = dfOBJ.df
    states = dfOBJ.states
    df.to_csv('utils/todays_data.csv', index=False)
    
    county_dfOBJ = CountiesDataFrame()
    county_df = county_dfOBJ.df
    county_df.to_csv('utils/todays_county_data.csv', index=False)
        
    
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

    ## clear click data
    @app.callback(
        Output('choropleth', 'clickData'),
        [Input('map-container', 'n_clicks'),
        Input('state_picker', 'value')]
    )
    def reset_clickData(n_clicks, state):
        return None

    # ## set the state picked based on click data
    # @app.callback(
    #     Output('state_picker', 'value'),
    #     [Input('choropleth', 'clickData')]
    # )
    # def update_states(clickData):
    #     if clickData == None:
    #         return dash.no_update
    #     else:
    #         try:
    #             test = int(clickData["points"][0]["location"])
    #             return dash.no_update
    #         except:
    #             state = clickData["points"][0]["location"]
    #             return state

    
    
    ## set the slider output
    @app.callback(
        Output('slider-output', 'children'),
        [Input('period-slider', 'value')]
    )
    def get_slider_value(value):
        return '{} weeks'.format(value)

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
                return daily_stats(state, period)
            else:
                return daily_stats(original_state, period)
            
        except:
            return daily_stats(original_state, period)
        

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
            

    ## existing-vs-new-chart
    # @app.callback(
    #     [Output("existing-vs-new", "figure")],
    #     [Input("state_picker", "value"),
    #     Input("period-slider", "value")]
    # )
    # def existing_vs_new_chart_callback(state, period):
    #     fig = existing_vs_new_chart(state, period)
    #     return [fig]

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
            
        # else:
        #     try:
        #         county = clickData["points"][0]["customdata"][0]
        #         fig = existing_vs_new_chart_counties(state, county, period)
        #         return [fig]
        #     except:
        #         state = clickData["points"][0]["location"]
        #         fig = existing_vs_new_chart(state, period)
        #         return [fig]

    ## positive-pct-chart title
    @app.callback(
    [Output("positive-pct-title", "children")],
    [Input("state_picker", "value"),
    Input("choropleth", "hoverData")],
    )                                                   # pylint: disable=W0612
    def positive_pct_title_callback(state, hoverData):
        original_state = state
        if hoverData == None:
            return ["{}: Positive % Over Time".format(state)]
        else:
            state = hoverData["points"][0]["location"]
            if state in states:
                return ["{}: Positive % Over Time".format(state)]
            else:
                return ["{}: Positive % Over Time".format(original_state)]




    # ## positive-pct-chart US ONLY
    # @app.callback(
    #     [Output("positive-pct", "figure")],
    #     [Input("state_picker", "value")]
    # )
    # def positive_pct_chart_callback(state):
    #     if state == 'U.S.' or state == 'United States':
    #         return [positive_pct_chart(state, df)]
    #     else:
    #         dash.no_update

    ## positive-pct-chart
    @app.callback(
        [Output("positive-pct", "figure")],
        [Input("state_picker", "value"),
        Input("choropleth", "hoverData")]
    )
    def positive_pct_chart_callback(state, hoverData):
        original_state = state
        if hoverData == None:
            return [positive_pct_chart(state, df)]
        else:
            state = hoverData["points"][0]["location"]
            if state in states:
                return [positive_pct_chart(state, df)]
            else:
                return [positive_pct_chart(original_state, df)]
          
            
       
        

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
            return create_cards(state, period)

    
    ## for printing click data
    # @app.callback(
    #     Output('click-data', 'children'),
    #     [Input('choropleth', 'hoverData')]
    # )
    # def display_click_data(clickData):
    #     return json.dumps(clickData, indent=2)

    
     

        


