import pandas as pd   
import numpy as np   
import dash_bootstrap_components as dbc    
import dash_html_components as html  

import sys
sys.path.append('../')
from utils import StatesDataFrame

GREEN = '#0CCE6B'
RED = '#B76D68'


def get_daily_stats(state, period, df):
    # df = pd.read_csv('utils/todays_data.csv')
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")

    if state=='United States':
        data = df.groupby('date').agg({'positive':'sum', 'new positive cases (last 7 days)':'sum', 'new deaths (last 7 days)':'sum', 'new negative cases (last 7 days)': 'sum', 'new positive cases':'sum', 'new negative cases': 'sum', 'positive case pct': 'mean', 'death rate (last 7 days)': 'mean'})
        # data = df.groupby('date').mean()[['positive cases rate of change (last 7 days average)', 'positive case pct rate of change (last 7 days average)', 'testing rate of change (last 7 days average)']]
        data = data.sort_values(by='date')
        
    else:
        data = df[df['state'] == state][['date', 'new negative cases', 'new positive cases (last 7 days)', 'new deaths (last 7 days)', 'new negative cases (last 7 days)', 'new positive cases', 'positive case pct', 'death rate (last 7 days)']]
        data = data.sort_values(by='date')
        

    data['period positives'] = data['new positive cases (last 7 days)'].shift(period*7)
    data['period deaths'] = data['new deaths (last 7 days)'].shift(period*7)
    data['period positive pct'] = data['positive case pct'].shift(period*7)
    data['period death rate'] = data['death rate (last 7 days)'].shift(period*7)

    data['% Difference positives'] = ((data['new positive cases (last 7 days)'] - data['period positives'])/data['period positives'])*100
    data['% Difference deaths'] = ((data['new deaths (last 7 days)'] - data['period deaths'])/data['period deaths'])*100
    data['Difference positive pct'] = (data['positive case pct'] - data['period positive pct'])
    data['Difference death rate'] = (data['death rate (last 7 days)'] - data['period death rate'])
    data = data.sort_values(by='date')
    data = data.tail(1)

    new_positives = int(data['new positive cases (last 7 days)'].to_numpy()[0])
    perc_change = data['% Difference positives'].to_numpy()[0]
    if perc_change > 0.0:
        positives_color = RED
    elif perc_change < 0.0:
        positives_color = GREEN

    new_deaths = int(data['new deaths (last 7 days)'].to_numpy()[0])
    perc_change_deaths = data['% Difference deaths'].to_numpy()[0]
    if perc_change_deaths > 0.0:
        deaths_color = RED
    elif perc_change_deaths < 0.0:
        deaths_color = GREEN

    positive_rate = data['positive case pct'].to_numpy()[0]
    positive_rate_change = data['Difference positive pct'].to_numpy()[0]
    if positive_rate_change > 0.0:
        positive_rate_color = RED
    elif positive_rate_change < 0.0:
        positive_rate_color = GREEN

    death_rate = data['death rate (last 7 days)'].to_numpy()[0]
    death_rate_change = data['Difference death rate'].to_numpy()[0]
    if death_rate_change > 0.0:
        death_rate_color = RED
    elif death_rate_change < 0.0:
        death_rate_color = GREEN

    stats = {
        'Positive Cases*': [new_positives, perc_change, positives_color],
        'Positive Rate*': [positive_rate, positive_rate_change, positive_rate_color],
        'Deaths*': [new_deaths, perc_change_deaths, deaths_color],
        'Death Rate*': [death_rate, death_rate_change, death_rate_color]
    }
    return stats

def get_daily_counties(county, state, period, df, county_df):
    ## county data - new cases
    county_df['date'] = pd.DatetimeIndex(county_df['date']).strftime("%Y-%m-%d")
    county_data = county_df[(county_df['state'] == state) & (county_df['county'] == county)]
    county_data['period positives'] = county_data['new positive cases (last 7 days)'].shift(period*7)
    county_data['% Difference positives'] = ((county_data['new positive cases (last 7 days)'] - county_data['period positives'])/county_data['period positives'])*100
   
    county_data = county_data.tail(1)
    ## state data - positive percentage
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")
    if state=='United States':
        data = df.groupby('date').agg({'positive':'sum', 'new positive cases (last 7 days)':'sum', 'new negative cases (last 7 days)': 'sum', 'new positive cases':'sum', 'new negative cases': 'sum', 'positive case pct': 'mean'})
        # data = df.groupby('date').mean()[['positive cases rate of change (last 7 days average)', 'positive case pct rate of change (last 7 days average)', 'testing rate of change (last 7 days average)']]
        data = data.sort_values(by='date')
        
    else:
        data = df[df['state'] == state][['date', 'new negative cases', 'new positive cases (last 7 days)', 'new negative cases (last 7 days)', 'new positive cases', 'positive case pct']]
        data = data.sort_values(by='date')
        

    data['period positive pct'] = data['positive case pct'].shift(period*7)
    
    data['Difference positive pct'] = (data['positive case pct'] - data['period positive pct'])
    data = data.sort_values(by='date')
    data = data.tail(1)

    ## from county
    new_positives = int(county_data['new positive cases (last 7 days)'].to_numpy()[0])
    perc_change = county_data['% Difference positives'].to_numpy()[0]
    if perc_change > 0.0:
        positives_color = RED
    elif perc_change < 0.0:
        positives_color = GREEN

    ## from state
    positive_rate = data['positive case pct'].to_numpy()[0]
    positive_rate_change = data['Difference positive pct'].to_numpy()[0]
    if positive_rate_change > 0.0:
        positive_rate_color = RED
    elif positive_rate_change < 0.0:
        positive_rate_color = GREEN

    stats = {
        'Positive Cases*': [new_positives, perc_change, positives_color],
        'Positive Rate*': [positive_rate, positive_rate_change, positive_rate_color]
    }
    print(stats)
    return stats
    

def daily_stats(county, state, period, df, county_df):
    print(county)
    if county == None:
        locator = state
        stats = get_daily_stats(state, period, df)
    else:
        locator = county
        stats = get_daily_counties(county, state, period, df, county_df)
    # print(stats)
    cards = []
    for key, value in stats.items():
        if key == 'Positive Cases*' or key == 'Deaths*':
            card_content = [
                dbc.CardHeader("{}% change".format(round(value[1], 0)),
                                    style = {"color": value[2]}),
                dbc.CardBody(
                    [
                        html.H3(f"{value[0]:,d}", className="Card header"),
                        html.P(
                            f"{key} - {locator}",
                            className="card-text"
                        )
                    ]
                )
            ]
            card = dbc.Col(dbc.Card(card_content, color="dark", inverse=True))
            cards.append(card)
    
        else:
            card_content = [
                dbc.CardHeader("{}% change".format(round(value[1]*100, 1)),
                                    style = {"color": value[2]}),
                dbc.CardBody(
                    [
                        html.H3(f"{round(value[0]*100, 1)}%", className="Card header"),
                        html.P(
                            f"{key} - {state}",
                            className="card-text"
                        )
                    ]
                )
            ]
            card = dbc.Col(dbc.Card(card_content, color="dark", inverse=True))
            cards.append(card)
    cards = html.Div(
        [
            dbc.Row(
                cards,
                className = "mb-4"
            )
        ]
    )
    return cards