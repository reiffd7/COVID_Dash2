import dash_bootstrap_components as dbc 
import dash_core_components as dcc       
import dash_html_components as html  
import dash_table
from dash_table.Format import Format

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

desktop_body = [
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dbc.Row([
                        dbc.Col(
                            
                                    [
                                       dcc.Slider(
                                            id='period-slider',
                                            min=2,
                                            max=10,
                                            step=1,
                                            value=10,
                                            
                                    ),
                                    html.Div(id='slider-output', style={"padding-left":"3vh"}) 
                                    ],
                                    style={"height": "10vh"},
                                
                            
                        ),
                        
                    ]

                    )
                ),
                width=2
            ),
            dbc.Col(
                html.Div(
                    dbc.Row(
                    id = 'daily-stats'
                    )
                ),
                width=7,
                style={'padding-left':'10%'}
            )
            
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dbc.Row(
                        [
                            # Chart 1
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                id = "existing-vs-new-chart-title",
                                                className="bottom-chart-h1-title"
                                            ),
                                            html.Div(
                                                [html.A("Learn More", href='https://towardsdatascience.com/data-visualization-of-covid-19-in-the-us-1881938aaf17', style={'color': '#468C98'})],

                                                className="bottom-chart-h2-title"
                                            ),
                                            html.Div(
                                                dcc.Loading(
                                                    dcc.Graph(
                                                        id="existing-vs-new",
                                                        config={"responsive": False},
                                                        style={"height": "30vh"},
                                                        className="top-bottom-left-chart-figure"
                                                    )
                                                ),
                                                id="chart-container"
                                            )
                                        ]
                                    )
                                ),
                                className="top-bottom-left-chart",
                                width=6,
                            ),
                            # Chart 2
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                id = "positive-pct-title",
                                                className="bottom-chart-h1-title"
                                            ),
                                            html.Div(
                                                "***",
                                                className="bottom-chart-h2-title"
                                            ),
                                            html.Div(
                                                dcc.Loading(
                                                    dcc.Graph(
                                                        id="positive-pct",
                                                        config={"responsive": False},
                                                        style={"height": "30vh"},
                                                        className="top-bottom-mid-chart-figure"
                                                    )
                                                ),
                                                id="chart-container"
                                            )
                                        ]
                                    )
                                ),
                                className="top-bottom-mid-chart",
                                width=6
                            )
                        ]
                    )
                ),
            className="bottom-chart-row",
            )
        ],
        className = "h-75"
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dbc.CardBody(
                        [
                            html.Div(
                                    dcc.Graph(
                                    id="choropleth",
                                    style={"height": "40vh"},
                                    clear_on_unhover = True
                                )
                            )
                            
                        ]
                    ),
                    id='map-container'
                )
            )
        ]
    ),
    dbc.Row(
        id='sim-states'
    ),
    dbc.Row(
        dbc.Col(
            html.Pre(
                id='click-data',
                style = styles['pre']
            )
        )
    )
]