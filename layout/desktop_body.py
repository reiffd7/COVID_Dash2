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

################ TABS STYLING ####################

font_size = ".9vw"
color_active = "#F4F4F4"
color_inactive = "#AEAEAE"
color_bg = "#010914"

tabs_styles = {
    "flex-direction": "row",
    "width": "5vw"
}
tab_style = {
    "padding": "1.3vh",
    "color": color_inactive,
    "fontSize": font_size,
    "backgroundColor": color_bg,
    "width": "5vw"
}

tab_selected_style = {
    "fontSize": font_size,
    "color": color_active,
    "padding": "1.3vh",
    "backgroundColor": color_bg,
    "width": "5vw"
}


## States Dropdown and Period Slider for the Navbar
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


## US Map
us_maps_tabs = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Tabs(
                            id="map-criteria",
                            value="cases",
                            children=[
                                dcc.Tab(
                                    label="Cases",
                                    value="cases",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Deaths",
                                    value="deaths",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                            ],
                            style=tabs_styles,
                            colors={
                                "border": None,
                                "primary": None,
                                "background": None,
                            },
                        )
                    ),
                ],
                className="d-flex justify-content-between top-bar-us-map-heading-content",
            ),
            html.Div(
                dcc.Loading(
                dcc.Graph(
                    id="choropleth",
                    style={"height": "40vh"},
                    clear_on_unhover=True
                ),),
                id="map-container",
            ),
        ]
    ),
    style={'background-color': '#272B30'}
)


## US Map
us_maps_animate = dbc.Card(
    id="choropleth_animate",
    style={'background-color': '#272B30'}
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
            dbc.Col(
                
                id = 'daily-stats',
                width=12
            )
            
        ],
        className = "h-75"
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
                us_maps_tabs
                # html.Div(
                #     dbc.CardBody(
                #         [
                #             html.Div(
                #                 dcc.Loading(
                #                     dcc.Graph(
                #                     id="choropleth",
                #                     style={"height": "40vh"},
                #                     clear_on_unhover = True
                #                 )
                #                 )
                #             )
                            
                #         ]
                #     ),
                #     id='map-container'
                # )
            )
        ]
    ),
    # dbc.Row(
    #     [
    #         dbc.Col(
    #             us_maps_animate
    #             # html.Div(
    #             #     dbc.CardBody(
    #             #         [
    #             #             html.Div(
    #             #                 dcc.Loading(
    #             #                     dcc.Graph(
    #             #                     id="choropleth",
    #             #                     style={"height": "40vh"},
    #             #                     clear_on_unhover = True
    #             #                 )
    #             #                 )
    #             #             )
                            
    #             #         ]
    #             #     ),
    #             #     id='map-container'
    #             # )
    #         )
    #     ]
    # ),
    dbc.Row(
        dbc.Col(
            [html.Button('Find My Location', id='input-on-submit'),
            html.Pre(
                id='ip-data'
            )]
        )
    ),
    dbc.Row(
        dbc.Col(
                [dcc.Dropdown(
                id= "sim-state-criteria",
                options=[{'label': 'Per Capita', 'value': 'Per Capita'},
                        {'label': 'Dynamics', 'value': 'Dynamics'},
                        {'label': 'Testing', 'value': 'Testing'},
                        {'label': 'Deaths', 'value': 'Deaths'},
                        {'label': 'Cases', 'value': 'Cases'}],
                value=['Cases', 'Testing'],
                multi=True,
                style={"background": "#272B30", "color": "#272B30"}
            ),
            html.Div(
                id='sim-states'
            )]
    )
    )
    
    
]