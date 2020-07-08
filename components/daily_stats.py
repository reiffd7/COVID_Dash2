import pandas as pd   
import numpy as np   
import dash_bootstrap_components as dbc    
import dash_html_components as html  

import sys
sys.path.append('../')
from utils import StatesDataFrame

GREEN = '#0CCE6B'
RED = '#B76D68'


def get_daily_stats(state, period):
    df = pd.read_csv('utils/todays_data.csv')
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")

    if state=='United States':
        data = df.groupby('date').agg({'positive':'sum', 'new positive cases (last 7 days)':'sum', 'new negative cases (last 7 days)': 'sum', 'new positive cases':'sum', 'new negative cases': 'sum', 'positive case pct': 'mean'})
        # data = df.groupby('date').mean()[['positive cases rate of change (last 7 days average)', 'positive case pct rate of change (last 7 days average)', 'testing rate of change (last 7 days average)']]
        data = data.sort_values(by='date')
        
    else:
        data = df[df['state'] == state][['date', 'new negative cases', 'new positive cases (last 7 days)', 'new negative cases (last 7 days)', 'new positive cases', 'positive case pct']]
        data = data.sort_values(by='date')
        

    data['period positives'] = data['new positive cases (last 7 days)'].shift(period*7)
    data['period positive pct'] = data['positive case pct'].shift(period*7)
    
    data['% Difference positives'] = ((data['new positive cases (last 7 days)'] - data['period positives'])/data['period positives'])*100
    data['Difference positive pct'] = (data['positive case pct'] - data['period positive pct'])
    data = data.sort_values(by='date')
    data = data.tail(1)

    new_positives = int(data['new positive cases (last 7 days)'].to_numpy()[0])
    perc_change = data['% Difference positives'].to_numpy()[0]
    if perc_change > 0.0:
        positives_color = RED
    elif perc_change < 0.0:
        positives_color = GREEN

    positive_rate = data['positive case pct'].to_numpy()[0]
    positive_rate_change = data['Difference positive pct'].to_numpy()[0]
    if positive_rate_change > 0.0:
        positive_rate_color = RED
    elif positive_rate_change < 0.0:
        positive_rate_color = GREEN

    stats = {
        'Positive Cases (in last 7 days)': [new_positives, perc_change, positives_color],
        'Positive Rate (in last 7 days)': [positive_rate, positive_rate_change, positive_rate_color],
        'INFO' : [df['date'].max()]
    }
    return stats

def daily_stats(state, period):
    stats = get_daily_stats(state, period)
    cards = []
    for key, value in stats.items():
        if key == 'Positive Cases (in last 7 days)':
            card = dbc.Col(
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.P(
                                    "{}%".format(round(value[1], 0)),
                                    style = {"color": value[2]}
                                ),
                                html.H1(
                                    f"{value[0]:,d}"
                                ),
                                html.P(
                                    f"{key}"
                                )
                            ]
                        ),
            
                    ),
                    width=4
                )
            cards.append(card)
        elif key == 'INFO':
            card = dbc.Col(
                    dbc.Col(
                        dbc.Row(
                            [
                                
                                html.H1(
                                    "Hover over states to view case growth and positive % graphs.",
                                    style = {"font-size": "15px"}
                                ),
                                html.H1(
                                    "Hover over counties to view case growth compared to their state.",
                                    style = {"font-size": "15px"}
                                ),
                                html.P(
                                    "Updated: {}".format(value[0]),
                                    style = {"font-weight": "bold", "color":"#BB9F06"}
                                )
                            ],
                            
                        ),
            
                    ),
                    width=4
            )
            cards.append(card)
        else:
            card = dbc.Col(
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.P(
                                    "{}%".format(round(value[1]*100, 1)),
                                    style = {"color": value[2]}
                                ),
                                html.H1(
                                    f"{round(value[0]*100, 1)}%"
                                ),
                                html.P(
                                    f"{key}"
                                )
                            ]
                        ),
            
                    ),
                    width=4
                )
            cards.append(card)
    return cards