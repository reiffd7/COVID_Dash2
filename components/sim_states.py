import dash_bootstrap_components as dbc 
import dash_core_components as dcc       
import dash_html_components as html  
import dash_table
from dash_table.Format import Format
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd    
import numpy as np 
import json


import sys
sys.path.append('../')
from utils import StatesDataFrame, StateFlags


with open('web_scraping/states.json', 'r') as f:
    states = json.load(f)
stateAbbrevs = {v: k for k,v in states.items()}

def get_top_five_sim(state, period):
    df = pd.read_csv('utils/todays_data.csv')
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")
    df = df[['state', 'date', 'new positive cases (last 7 days)', 'positive case pct']]
    df['cases_period'] = df.groupby('state')['new positive cases (last 7 days)'].shift(period*7)
    df['pct_period'] = df.groupby('state')['positive case pct'].shift(period*7)
    df = df[df['date'] == df['date'].max()]
    df['cases diff'] = (df['new positive cases (last 7 days)'] - df['cases_period'])/(df['cases_period'])
    df['pct diff'] = (df['positive case pct'] - df['pct_period'])/(df['pct_period'])
    df = df.set_index('state')
    sim_list = []
    states = df.index.to_numpy()
    a = df.loc[state][['positive case pct', 'cases diff', 'pct diff']].to_numpy()
    for stateB in states:
        b = df.loc[stateB][['positive case pct', 'cases diff', 'pct diff']].to_numpy()
        similarity = cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))
        if stateB != state:
            entry = {'state': stateB, 'similarity': similarity[0][0]}
            sim_list.append(entry)
    sim_df = pd.DataFrame(sim_list).sort_values(by='similarity', ascending=False)
    return sim_df['state'].to_numpy()[:5]

def create_cards(state, period):
    top_5_states = get_top_five_sim(state, period)
    cards = []
    for i, state in enumerate(top_5_states):
        img_url = StateFlags[state]
        entry = dbc.Col(
                html.Div(
                    dbc.Card(
                        dbc.CardBody(
                    [
                        html.Div(
                            '{}:  {}'.format(i+1,stateAbbrevs[state])
                        ),
                        html.Div(
                            html.Img(src=img_url, style={'height':'60%', 'width':'60%'})
                        )
                    ]
                        )
                    )
                )
            )
        cards.append(entry)

    return cards
        



