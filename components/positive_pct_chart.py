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



def positive_pct_chart(state, df):

    df = df[(df['positive case pct'] < 1.0) & (df['positive case pct'] >= 0.0)]
    df['date'] = pd.DatetimeIndex(df['date']).strftime("%Y-%m-%d")
    df = df[df['date'] >= '2020-04-01']
    if state == 'United States':
        # df = df[df['date'] != '2020-06-11']
        print('fire')
        data = df.groupby('date').agg({'positive case pct': 'mean'})
        
        data = data.reset_index().sort_values(by='date')
    else:
        data = df[df['state'] == state]
        data = data[['date', 'positive case pct']]

    # data['positives in period'] = data['new positive cases'].rolling(period*7, min_periods=0).sum()
    # data['negatives in period'] = data['new negative cases'].rolling(period*7, min_periods=0).sum()
    # data['positive pct in period'] = data['positives in period']/(data['positives in period'] + data['negatives in period'])
    ys = data['positive case pct']
    xs = data['date']
    # length = math.ceil(max(max(ys), max(xs)))
    # annotation_x = length+1
    # annotation_y = length+1
    template_new = "%{customdata} positive pct on %{text}<extra></extra>"
    monthDict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August'}
    data['month'] = pd.to_datetime(data['date']).apply(lambda x: monthDict[x.month])
    fig = go.Figure()
    for month in monthDict.values():
        monthly_data = data[data['month'] == month]
        ys = monthly_data['positive case pct']
        xs = monthly_data['date']
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                text = monthly_data['date'],
                mode = 'markers+lines',
                name=month,
                customdata = [human_format(x) for x in monthly_data['positive case pct'].to_numpy()],
                hovertemplate=template_new,
                showlegend = True

            )
        )
    # fig.add_trace(
    #     go.Scatter(
    #         x=list(range(0, length+1)),
    #         y=list(range(0, length+1)),
    #         mode="lines",
    #         text = None,
    #         name="Exponential Growth",
    #         line= dict(color='#941B0C', dash='dash'),
            

    #     )
    # )
    # fig.add_annotation(
    #     x=annotation_x,
    #     y=annotation_y,
    #     text='Exponential Growth',
    #     font={'size': 10},
    #     xshift=-65,
    #     showarrow=False
    # )
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
        yaxis_title="positive % (last 7 days)",
        xaxis = {"title" : {"text" : "Date", "standoff" : 0}}
    )
    return fig



    