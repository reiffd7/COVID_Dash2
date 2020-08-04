import pandas as pd
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity



with open('web_scraping/states.json', 'r') as f:
    states = json.load(f)
stateAbbrevs = {v: k for k,v in states.items()}
with open('web_scraping/statePop.json', 'r') as f:
    statePops = json.load(f)

COVID_METRICS = ['positive', 'negative', 'death', 
            'inIcuCurrently', 'onVentilatorCurrently', 
            'hospitalizedCurrently', 'new positive cases', 'new negative cases', 'deathIncrease',  
            'new positive cases (last 7 days)','new negative cases (last 7 days)', 'tests (last 7 days)', 'new deaths (last 7 days)'
            'death rate (last 7 days)', 'positive rate (last 7 days average)', 'tests (last 7 days per capita)', 'new deaths (per capita)',
            'new positive (per capita)', 'Hospitalized (per capita)', 'In ICU (per capita)', 'On Ventilator (per capita)', 'testing rate of change (last 7 days average)',	
            'positive case pct rate of change (last 7 days average)',	'positive cases rate of change (last 7 days average)', 'death pct rate of change']

DYNAMICS = ['state','testing rate of change (last 7 days average)',	
            'positive case pct rate of change (last 7 days average)',	'positive cases rate of change (last 7 days average)']

PER_CAPITA = ['state','tests (last 7 days per capita)', 'new deaths (per capita)', 'death rate (last 7 days)', 'positive case pct',
            'new positive (per capita)', 'Hospitalized (per capita)', 'In ICU (per capita)', 'On Ventilator (per capita)']

ABSOLUTE_RECENT = ['state','inIcuCurrently', 'onVentilatorCurrently', 
            'hospitalizedCurrently', 'new positive cases', 'new negative cases', 'deathIncrease',  
            'new positive cases (last 7 days)','new negative cases (last 7 days)', 'tests (last 7 days)', 'new deaths (last 7 days)']

ABSOLUTE_TOTAL = ['state','positive', 'negative', 'death']



class CountiesDataFrame(object):

    def __init__(self):
        url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
        self.df = pd.read_csv(url, parse_dates=['date']).sort_index()
        self.Clean()
        self.AddCalculatedFields()


    def Clean(self):
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['state'] = self.df['state'].apply(lambda x: states[x])
        self.df = self.df.dropna(subset=['fips'])
        self.df['fips'] = self.df['fips'].astype(int)

    def AddCalculatedFields(self):
        self.df['new positive cases'] = self.df.groupby(['fips'])['cases'].diff(1).fillna(0)
        self.df['new positive cases (last 7 days)'] = self.df.groupby(['fips'])['new positive cases'].apply(lambda x: x.rolling(7, min_periods=0).sum())
        self.df['new deaths'] = self.df.groupby(['fips'])['deaths'].diff(1).fillna(0)
        self.df['new deaths (last 7 days)'] = self.df.groupby(['fips'])['new deaths'].apply(lambda x: x.rolling(7, min_periods=0).sum())
        self.df['death rate (last 7 days)'] = self.df['new deaths (last 7 days)']/self.df['new positive cases (last 7 days)']


class StatesDataFrame(object):

    def __init__(self):
        url = 'https://covidtracking.com/api/v1/states/daily.csv'
        self.df = pd.read_csv(url, parse_dates=['date']).sort_index()
        print('cleaning')
        self.Clean()
        self.AddCalculatedFields()
        self.dates = self.df['date'].unique()
        self.states = sorted(list(self.df['state'].unique()))
        self.BASIC_COLS = ['date', 'state', 'new positive cases']
        self.COVID_METRICS = ['positive', 'negative', 'death', 'hospitalizedCurrently', 'new positive cases', 'new negative cases', 
                        'new positive cases (last 7 days)','new negative cases (last 7 days)', 'tests last week',	
                        'tests last week (per capita)',	'testing rate of change', 'testing rate of change (last 7 days average)',	
                        'positive case pct', 'positive case pct (last 7 days average)',	'zero',	'positive case pct rate of change',	
                        'positive case pct rate of change (last 7 days average)',	'positive cases rate of change',	
                        'positive cases rate of change (last 7 days average)']

    def Clean(self):
        self.df = self.df[['date', 'state', 'fips', 'positive', 'negative', 'death', 'hospitalizedCurrently', 'inIcuCurrently', 'onVentilatorCurrently', 'deathIncrease']]
        self.df['date'] =  pd.to_datetime(self.df['date'])
        self.df = self.df[~self.df['state'].isin(['MP', 'GU', 'AS', 'PR', 'VI'])]
        

    def AddCalculatedFields(self):
        self.df.sort_values(by=['state', 'date'], inplace=True)
        self.df = self.df.reset_index()

        ## Basic Info - Positives/Negatives/Deaths/Tests - In the last week
        self.df['new positive cases'] = self.df.groupby(['state', 'fips'])['positive'].diff(1).fillna(0)
        self.df['new negative cases'] = self.df.groupby(['state', 'fips'])['negative'].diff(1).fillna(0)
        self.df['new deaths'] = self.df['deathIncrease']
        self.df['new negative cases (last 7 days)'] = self.df.groupby(['state', 'fips'])['new negative cases'].apply(lambda x: x.rolling(7, min_periods=0).sum())
        self.df['new positive cases (last 7 days)'] = self.df.groupby(['state', 'fips'])['new positive cases'].apply(lambda x: x.rolling(7, min_periods=0).sum())
        self.df['new deaths (last 7 days)'] = self.df.groupby(['state', 'fips'])['new deaths'].apply(lambda x: x.rolling(7, min_periods=0).sum())
        self.df['tests (last 7 days)'] = self.df['new positive cases (last 7 days)'] + self.df['new negative cases (last 7 days)']

        ## Percentages - Death/Positive Rate
        self.df['death rate (last 7 days)'] = self.df['new deaths (last 7 days)']/self.df['new positive cases (last 7 days)']
        self.df['positive case pct'] = self.df['new positive cases (last 7 days)']/self.df['tests (last 7 days)']

        ## Per Capita 
        self.df['new deaths (per capita)'] = self.df.apply(lambda x: x['new deaths (last 7 days)']/statePops[stateAbbrevs[x['state']]], axis=1)
        self.df['Hospitalized (per capita)'] = self.df.apply(lambda x: x['hospitalizedCurrently']/statePops[stateAbbrevs[x['state']]], axis=1)
        self.df['In ICU (per capita)'] = self.df.apply(lambda x: x['inIcuCurrently']/statePops[stateAbbrevs[x['state']]], axis=1)
        self.df['On Ventilator (per capita)'] = self.df.apply(lambda x: x['onVentilatorCurrently']/statePops[stateAbbrevs[x['state']]], axis=1)
        self.df['new positive (per capita)'] = self.df.apply(lambda x: x['new positive cases (last 7 days)']/statePops[stateAbbrevs[x['state']]], axis=1)
        self.df['tests (last 7 days per capita)'] = self.df.apply(lambda x: x['tests (last 7 days)']/statePops[stateAbbrevs[x['state']]], axis=1)


        ## Rates of Change
        self.df['testing rate of change'] = (self.df['tests (last 7 days)'] - self.df.groupby(['state', 'fips'])['tests (last 7 days)'].shift(1).fillna(0))/(self.df.groupby(['state', 'fips'])['tests (last 7 days)'].shift(1).fillna(0))
        self.df['testing rate of change (last 7 days average)'] = self.df.groupby(['state', 'fips'])['testing rate of change'].apply(lambda x: x.rolling(7, min_periods=0).mean()).fillna(0)
        self.df['death pct rate of change'] = self.df['death rate (last 7 days)'] - self.df.groupby(['state', 'fips'])['death rate (last 7 days)'].shift(1).fillna(0)
        self.df['positive case pct rate of change'] = self.df['positive case pct'] - self.df.groupby(['state', 'fips'])['positive case pct'].shift(1).fillna(0)
        self.df['positive case pct rate of change (last 7 days average)'] = self.df.groupby(['state', 'fips'])['positive case pct rate of change'].apply(lambda x: x.rolling(7, min_periods=0).mean()).fillna(0)
        self.df['positive cases rate of change'] = (self.df['new positive cases (last 7 days)'] - self.df.groupby(['state', 'fips'])['new positive cases (last 7 days)'].shift(1))/(self.df['positive'] - self.df.groupby(['state', 'fips'])['positive'].shift(1)).fillna(0)
        self.df['positive cases rate of change (last 7 days average)'] = self.df.groupby(['state', 'fips'])['positive cases rate of change'].apply(lambda x: x.rolling(7, min_periods=0).mean()).fillna(0)

        self.df['date'] = pd.to_datetime(self.df['date'].apply(lambda x: str(x).split('T')[0]))
        self.df.sort_values(by=['date', 'state'], inplace=True)

df = pd.read_csv('utils/todays_data.csv')
STATE_LABELS = [{'label': i, 'value': i} for i in sorted(list(df['state'].unique()))]
STATE_LABELS.insert(0, {'label': 'U.S.', 'value': 'United States'})


# def cosine_similarity(state):
#     df = StatesDataFrame().df



COORDS = {"AL": {"lat": 32.806671, "long": -86.79113}, 
        "AK": {"lat": 61.370716, "long": -152.404419}, 
        "AZ": {"lat": 33.729759, "long": -111.431221}, 
        "AR": {"lat": 34.969704, "long": -92.373123}, 
        "CA": {"lat": 36.116203, "long": -119.681564}, 
        "CO": {"lat": 39.059811, "long": -105.311104}, 
        "CT": {"lat": 41.597782, "long": -72.755371}, 
        "DE": {"lat": 39.318523, "long": -75.507141}, 
        "DC": {"lat": 38.897438, "long": -77.026817}, 
        "FL": {"lat": 27.766279, "long": -81.686783}, 
        "GA": {"lat": 33.040619, "long": -83.643074}, 
        "HI": {"lat": 21.094318, "long": -157.498337}, 
        "ID": {"lat": 44.240459, "long": -114.478828}, 
        "IL": {"lat": 40.349457, "long": -88.986137}, 
        "IN": {"lat": 39.849426, "long": -86.258278}, 
        "IA": {"lat": 42.011539, "long": -93.210526}, 
        "KS": {"lat": 38.5266, "long": -96.726486}, 
        "KY": {"lat": 37.66814, "long": -84.670067}, 
        "LA": {"lat": 31.169546, "long": -91.867805}, 
        "ME": {"lat": 44.693947, "long": -69.381927}, 
        "MD": {"lat": 39.063946, "long": -76.802101}, 
        "MA": {"lat": 42.230171, "long": -71.530106}, 
        "MI": {"lat": 43.326618, "long": -84.536095}, 
        "MN": {"lat": 45.694454, "long": -93.900192}, 
        "MS": {"lat": 32.741646, "long": -89.678696}, 
        "MO": {"lat": 38.456085, "long": -92.288368}, 
        "MT": {"lat": 46.921925, "long": -110.454353}, 
        "NE": {"lat": 41.12537, "long": -98.268082}, 
        "NV": {"lat": 38.313515, "long": -117.055374}, 
        "NH": {"lat": 43.452492, "long": -71.563896}, 
        "NJ": {"lat": 40.298904, "long": -74.521011}, 
        "NM": {"lat": 34.840515, "long": -106.248482}, 
        "NY": {"lat": 42.165726, "long": -74.948051}, 
        "NC": {"lat": 35.630066, "long": -79.806419}, 
        "ND": {"lat": 47.528912, "long": -99.784012}, 
        "OH": {"lat": 40.388783, "long": -82.764915}, 
        "OK": {"lat": 35.565342, "long": -96.928917}, 
        "OR": {"lat": 44.572021, "long": -122.070938}, 
        "PA": {"lat": 40.590752, "long": -77.209755}, 
        "RI": {"lat": 41.680893, "long": -71.51178}, 
        "SC": {"lat": 33.856892, "long": -80.945007}, 
        "SD": {"lat": 44.299782, "long": -99.438828}, 
        "TN": {"lat": 35.747845, "long": -86.692345}, 
        "TX": {"lat": 31.054487, "long": -97.563461}, 
        "UT": {"lat": 40.150032, "long": -111.862434},
         "VT": {"lat": 44.045876, "long": -72.710686}, 
         "VA": {"lat": 37.769337, "long": -78.169968}, 
         "WA": {"lat": 47.400902, "long": -121.490494}, 
         "WV": {"lat": 38.491226, "long": -80.954453}, 
         "WI": {"lat": 44.268543, "long": -89.616508}, 
         "WY": {"lat": 42.755966, "long": -107.30249}}





def cosine_sim(state, sim_criteria):
    df = pd.read_csv('utils/todays_data.csv')
    df = df.fillna(0)
    df = df[df['date'] == max(df['date'])]
    df.drop(columns=['index', 'date', 'fips'], inplace=True)
    if sim_criteria == 'dynamics':
        df = df[DYNAMICS]
    if sim_criteria == 'per capita':
        df = df[PER_CAPITA]
    if sim_criteria == 'absolute (recent)':
        df = df[ABSOLUTE_RECENT]
    if sim_criteria == 'absolute (total)':
        df = df[ABSOLUTE_TOTAL]

    
    df = df.set_index('state')
    sim_list = []
    states = df.index.to_numpy()
    a = df.loc[state].fillna(0).to_numpy()
    for stateB in states:
        b = df.loc[stateB].fillna(0).to_numpy()
        try:
            similarity = cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))
            if stateB != state:
                entry = {'state': stateB, 'similarity': similarity[0][0]}
                sim_list.append(entry)
        except:
            print(stateB)
    simDf = pd.DataFrame(sim_list).sort_values(by='similarity', ascending=False)
    return simDf.head(10)


StateFlags = {k: 'https://www.nationsonline.org/flags_big/{}_state_flag.jpg'.format(v.replace(' ', '_')) for k,v in stateAbbrevs.items()}
StateFlags['DC'] = 'https://cdn.britannica.com/94/4994-004-F06634D5/Flag-District-of-Columbia.jpg'