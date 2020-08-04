import pandas as pd   
import numpy as np   
import plotly.graph_objects as go
import math

import sys
sys.path.append('../')
from utils import StatesDataFrame


def human_format(num):
    """Formats a number and returns a human-readable version of it in string
    form. Ex: 300,000 -> 300k
    :params num: number to be converted to a formatted string
    """
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(
            num
            ).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude]
    )



def existing_vs_new_chart(state, period, df):

    # df = pd.read_csv('utils/todays_data.csv')
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")
    # df = df[df['date'] >= '2020-04-20']
    if state == 'United States':
        data = df.groupby('date').sum()[[ 'new positive cases', 'new positive cases (last 7 days)']]
        data = data.reset_index().sort_values(by='date')
    else:
        data = df[df['state'] == state]
        data = data[['date',  'new positive cases', 'new positive cases (last 7 days)']]

    data['new positive in period'] = data['new positive cases'].rolling(period*7, min_periods=0).sum()
    monthDict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August'}
    data['month'] = pd.to_datetime(data['date']).apply(lambda x: monthDict[x.month])
    ys = np.log(data['new positive cases (last 7 days)'])
    xs = np.log(data['new positive in period'])
    length = math.ceil(max(max(ys), max(xs)))
    annotation_x = length+1
    annotation_y = length+1
    fig = go.Figure()
    for month in monthDict.values():
        monthly_data = data[data['month'] == month]
        ys = np.log(monthly_data['new positive cases (last 7 days)'])
        xs = np.log(monthly_data['new positive in period'])
        template_new = "%{customdata} new cases on %{text}<extra></extra>"
        
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                text = monthly_data['date'],
                name=month,
                customdata = [human_format(x) for x in monthly_data['new positive cases (last 7 days)'].to_numpy()],
                hovertemplate=template_new

            )
        )
    fig.add_trace(
        go.Scatter(
            x=list(range(0, length+1)),
            y=list(range(0, length+1)),
            mode="lines",
            text = None,
            showlegend=False,
            line= dict(color='#941B0C', dash='dash'),
            

        )
    )
    fig.add_annotation(
        x=annotation_x,
        y=annotation_y,
        text='Exponential Growth',
        font={'size': 10},
        xshift=-65,
        showarrow=False
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=np.log(ny['positive']),
    #         y=np.log(ny['new positive cases (last 7 days)']),
    #         name="Existing vs. New Cases",
    #         line={"color": "#F4B000"},
    #         customdata = [human_format(x) for x in data['new positive cases (last 7 days)'].to_numpy()],
    #         hovertemplate=template_new

    #     )
    # )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 1},
        template="plotly_dark",
        # annotations=annotations,
        autosize=True,
        showlegend=True,
        legend_orientation="h",
        paper_bgcolor="rgba(0,0,0,0)",
        #         paper_bgcolor="black",
        plot_bgcolor="rgba(0,0,0,0)",
        #         plot_bgcolor="black",
        # xaxis_title="Number of Days",
        yaxis={"linecolor": "rgba(0,0,0,0)"},
        hoverlabel={"font": {"color": "black"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
        yaxis_title="new positive cases (last 7 days)",
        xaxis = {"title" : {"text" : "new positive cases (last {} days)".format(period*7), "standoff" : 0}}
    )
    return fig


def existing_vs_new_chart_counties(state, county, period, county_df, data):

  
    data = data[data['state'] == state]
    data = data[['date', 'new positive cases', 'new positive cases (last 7 days)']]

    county_df = county_df[(county_df['county'] == county) & (county_df['state'] == state)]
    county_data = county_df[['date', 'cases', 'new positive cases', 'new positive cases (last 7 days)']]

    data['new positive in period'] = data['new positive cases'].rolling(period*7, min_periods=0).sum()
    county_data['new positive in period'] = county_data['new positive cases'].rolling(period*7, min_periods=0).sum()
    monthDict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August'}
    data['month'] = pd.to_datetime(data['date']).apply(lambda x: monthDict[x.month])
    ys = np.log(data['new positive cases (last 7 days)'])
    xs = np.log(data['new positive in period'])

    ys_c = np.log(county_data['new positive cases (last 7 days)'])
    xs_c = np.log(county_data['new positive in period'])

    length = math.ceil(max(max(ys), max(xs)))
    annotation_x = length+1
    annotation_y = length+1
    fig = go.Figure()
    template_new = "%{customdata} new cases on %{text}<extra></extra>"
    
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            text = data['date'],
            name = state,
            customdata = [human_format(x) for x in data['new positive cases (last 7 days)'].to_numpy()],
            hovertemplate=template_new

        )
    )
    fig.add_trace(
        go.Scatter(
            x=xs_c,
            y=ys_c,
            text = county_data['date'],
            name = county,
            customdata = [human_format(x) for x in county_data['new positive cases (last 7 days)'].to_numpy()],
            hovertemplate=template_new

        )
    )
    fig.add_trace(
        go.Scatter(
            x=list(range(0, length+1)),
            y=list(range(0, length+1)),
            mode="lines",
            text = None,
            showlegend=False,
            line= dict(color='#941B0C', dash='dash'),
            

        )
    )
    fig.add_annotation(
        x=annotation_x,
        y=annotation_y,
        text='Exponential Growth',
        font={'size': 10},
        xshift=-65,
        showarrow=False
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=np.log(ny['positive']),
    #         y=np.log(ny['new positive cases (last 7 days)']),
    #         name="Existing vs. New Cases",
    #         line={"color": "#F4B000"},
    #         customdata = [human_format(x) for x in data['new positive cases (last 7 days)'].to_numpy()],
    #         hovertemplate=template_new

    #     )
    # )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 1},
        template="plotly_dark",
        # annotations=annotations,
        autosize=True,
        showlegend=True,
        legend_orientation="h",
        paper_bgcolor="rgba(0,0,0,0)",
        #         paper_bgcolor="black",
        plot_bgcolor="rgba(0,0,0,0)",
        #         plot_bgcolor="black",
        # xaxis_title="Number of Days",
        yaxis={"linecolor": "rgba(0,0,0,0)"},
        hoverlabel={"font": {"color": "black"}},
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        font=dict(family="Roboto, sans-serif", size=10, color="#f4f4f4"),
        yaxis_title="new positive cases (last 7 days)",
        xaxis = {"title" : {"text" : "new positive cases (last {} days)".format(period*7), "standoff" : 0}}
    )
    return fig