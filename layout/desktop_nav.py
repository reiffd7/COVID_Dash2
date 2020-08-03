import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import sys
sys.path.append('../')
from utils import STATE_LABELS


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


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
                value=2,                                 
                ), width=3),
                dbc.Col(html.Div(id='slider-output', style={"padding-left":"3vh"}
                )),
                dbc.Col(dcc.Dropdown(
                    id="state_picker",
                    options=STATE_LABELS,
                    value="United States",
                    clearable=False,
                    searchable=False,
                    style={"background-color": "coral", 'width': '5vw'}
                ), width=3)
            ],
            no_gutters=True,
            className="ml-auto flex-nowrap mt-3 mt-md-0",
            style={'width': '50%'},
            align="center"
)


navbar = [
        html.A(
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
       dbc.Collapse(states_dropdown, id="navbar-collapse", navbar=True)                 
       
    ]








#### Example


# dropdown_bar = dbc.Row(
#     dbc.DropdownMenu(label="Location", children=[dbc.DropdownMenuItem("US"),]),
#     no_gutters=True,
#     className="dropdown-location-menu flex-nowrap mt-md-0",
#     align="center",
# )

# about_bar = dbc.Row(
#     dbc.NavbarBrand(
#         [
#             # html.A(
#             #     "CDC",
#             #     id="navbar-resources-link",
#             #     className="navbar-brand-links",
#             #     href="https://www.cdc.gov/coronavirus/2019-ncov/index.html",
#             #     target="_blank",
#             # ),
#             # html.A(
#             #     "World Health Organization",
#             #     id="navbar-resources-link",
#             #     className="navbar-brand-links",
#             #     href="https://www.who.int/emergencies/diseases/novel-coronavirus-2019",
#             #     target="_blank",
#             # ),
#             # html.A(
#             #     "Get Mobile Updates",
#             #     className="navbar-brand-links",
#             #     href=config.SMS_APP_URL,
#             #     id="get-mobile-updates",
#             # ),
#             # html.A(
#             #     "Vaccine Tracker",
#             #     className="navbar-brand-links",
#             #     href="https://pedantic-boyd-2e5947.netlify.com/"
#             # ),
#             html.A("About", className="navbar-brand-links", href="/about"),
#         ]
#     ),
#     className="ml-auto flex-nowrap mt-md-0",
#     align="center",
# )

# # User row and col to control vertical alignment of logo/brand
# navbar = [
#     dbc.Row(
#         [
#             # dbc.Col(
#             #     html.Img(src="assets/images/covid19-new-logo.png", height="30px")
#             # ),
#             dbc.Col(
#                 html.A(
#                     dbc.NavbarBrand(
#                         [
#                             html.P("COVID-19", className="navbar-brand-covid-19-text"),
#                             html.P("Tracker", className="navbar-brand-us-cases-text"),
#                         ]
#                     ),
#                     className="page-title-link",
#                     href="/",
#                 )
#             ),
#         ],
#         align="center",
#         no_gutters=True,
#     ),
#     dbc.NavbarToggler(id="navbar-toggler", className="navbar-toggler-1"),
#     # dbc.Collapse(dropdown_bar, id="navbar-collapse", navbar=True),
#     about_bar
#     # dbc.NavbarBrand(about_bar),
# ]