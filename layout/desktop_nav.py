import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import sys
sys.path.append('../')
from utils import STATE_LABELS


states_dropdown = dbc.Col(
    dcc.Dropdown(
                    id="state_picker",
                    options=STATE_LABELS,
                    value="United States",
                    clearable=False,
                    searchable=False,
                    className="states-dropdown",
                    style={'width':'80px'}
                )
)


navbar = [
    dbc.NavbarToggler(id="navbar-toggler", className="navbar-toggler-1"),
    dbc.Collapse(states_dropdown, 
                id="navbar-collapse",
                navbar=True),
        dbc.Col(
                html.A(
                    dbc.NavbarBrand(
                        [
                            html.P(id='page-title', className="navbar-brand-covid-19-text"),
                            # html.P("Analysis", className="navbar-brand-us-cases-text"),
                        ]
                    ),
                    className="page-title-link",
                    style={'font-family': 'Arial Black', 'font-size': '24px'},
                    href="/",
                ),
            style={'align': 'center', 'padding-right': '300px'}
            ),
        
        
    html.Img(id="flag", style={'height':'60px', 'width':'120px', 'padding-right': '10px'})
    # about_bar
    # # dbc.NavbarBrand(about_bar),
]
