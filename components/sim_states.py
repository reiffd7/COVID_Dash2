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

CRITERIA_DICT = {'Per Capita': ['new deaths (per capita)',
                                'Hospitalized (per capita)',
                                'In ICU (per capita)',
                                'On Ventilator (per capita)',
                                ],
                'Dynamics': ['testing rate of change (last 7 days average)',
                            'death pct rate of change',
                            'positive case pct rate of change (last 7 days average)',
                            'positive cases rate of change (last 7 days average)'],
                'Testing': ['tests (last 7 days)'],
                'Deaths': ['new deaths (last 7 days)', 
                            'new deaths'],
                'Cases': ['new positive cases',
                        'new positive cases (last 7 days)']}

def get_top_five_sim(state, df, criterias):
    # df = pd.read_csv('utils/todays_data.csv')
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")
    # df = df[['state', 'date', 'new positive cases (last 7 days)', 'positive case pct']]
    # df['cases_period'] = df.groupby('state')['new positive cases (last 7 days)'].shift(period*7)
    # df['pct_period'] = df.groupby('state')['positive case pct'].shift(period*7)
    df = df[df['date'] == df['date'].max()]
    # df['cases diff'] = (df['new positive cases (last 7 days)'] - df['cases_period'])/(df['cases_period'])
    # df['pct diff'] = (df['positive case pct'] - df['pct_period'])/(df['pct_period'])
    metrics = []
    if criterias == []:
        for v in CRITERIA_DICT.values():
            metrics.append(v)
    else:
        for criteria in criterias:
            metrics.append(CRITERIA_DICT[criteria])
    metrics = list(set([item for sublist in metrics for item in sublist]))
    df = df.set_index('state')
    df = df.fillna(0)
    sim_list = []
    states = df.index.to_numpy()
    a = np.nan_to_num(df.loc[state][metrics].to_numpy(), nan=0.0, posinf=0.0, neginf=0.0)
    for stateB in states:
        b = np.nan_to_num(df.loc[stateB][metrics].to_numpy(), nan=0.0, posinf=0.0, neginf=0.0)
        similarity = cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))
        if stateB != state:
            entry = {'state': stateB, 'similarity': similarity[0][0]}
            sim_list.append(entry)
    sim_df = pd.DataFrame(sim_list).sort_values(by='similarity', ascending=False)
    return sim_df['state'].to_numpy()[:5]

def create_cards(state, df, criterias):
    top_5_states = get_top_five_sim(state, df, criterias)
    cards = []
    for i, state in enumerate(top_5_states):
        img_url = 'https://dynamic-covid19-analysis.s3.us-east-2.amazonaws.com/{}.png'.format(state)
        if state == 'DC':
            img_url = 'https://cdn.britannica.com/94/4994-004-F06634D5/Flag-District-of-Columbia.jpg'
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

    return dbc.Row(cards)
        



