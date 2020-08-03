import dash_bootstrap_components as dbc 
import dash_core_components as dcc       
import dash_html_components as html  
import dash_table
from dash_table.Format import Format
import sys
sys.path.append('../')
from utils import STATE_LABELS

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

states_dropdown = dbc.Row(
            [
    
                dbc.Col(dcc.Slider(
                id='period-slider',
                min=2,
                max=10,
                step=1,
                marks={
                    1: '1w',
                    3: '3w',
                    5: '5w',
                    7: '7w',
                    9: '9w'
                },
                value=3,                                 
                ), width=3),
                dbc.Col(html.Div(id='slider-output', style={"padding-left":"3vh"}
                )),
                dbc.Col(dcc.Dropdown(
                    id="state_picker",
                    options=STATE_LABELS,
                    value="United States",
                    clearable=False,
                    searchable=False,
                    style={"background-color": "#F6AA1C", 'width': '5vw'}
                ), width=3)
            ],
            no_gutters=True,
            className="ml-auto flex-nowrap mt-3 mt-md-0",
            style={'width': '50%'},
            align="center"
)

desktop_body = [
    dbc.Navbar(
    [html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(id="flag", height="30px")),
                    dbc.Col(dbc.NavbarBrand(id='page-title'))
                ],
                align='center',
                no_gutters = True
            ),
            href="/"
        ),

       dbc.NavbarToggler(id="navbar-toggler"),
       dbc.Collapse(states_dropdown, id="navbar-collapse", navbar=True)],
    color="#010915",
    dark=True,
    className="desktop-navbar",
    sticky="top" 
    ),
    dbc.Row(
        [
            # dbc.Col(
            #     html.Div(
            #         dbc.Row([
            #             dbc.Col(
                            
            #                         [
            #                            dcc.Slider(
            #                                 id='period-slider',
            #                                 min=2,
            #                                 max=10,
            #                                 step=1,
            #                                 value=10,
                                            
            #                         ),
            #                         html.Div(id='slider-output', style={"padding-left":"3vh"}) 
            #                         ],
            #                         style={"height": "10vh"},
                                
                            
            #             ),
                        
            #         ]

            #         )
            #     ),
            #     width=2
            # ),
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
                                                    ),
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
                                                id = "pospct_title",
                                                className="bottom-chart-h1-title"
                                            ),
                                            html.Div(
                                                "***",
                                                className="bottom-chart-h2-title"
                                            ),
                                            html.Div(
                                                dcc.Loading(
                                                    dcc.Graph(
                                                        id="pospct_chart",
                                                        config={"responsive": False},
                                                        style={"height": "30vh"}
                                                    ),
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
                                dcc.Loading(
                                    dcc.Graph(
                                    id="choropleth",
                                    style={"height": "40vh"},
                                    clear_on_unhover = True
                                )
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
            [html.Button('Find My Location', id='input-on-submit'),
            html.Pre(
                id='ip-data',
                style = styles['pre']
            )]
        )
    )
]