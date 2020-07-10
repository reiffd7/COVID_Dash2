import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc    
import dash_html_components as html
from layout import build_desktop_layout
from callbacks import register_routes_callbacks, register_desktop_callbacks, register_desktop_callacks_data


external_stylesheets = [
    # Bootswatch theme
    dbc.themes.SLATE,
    # for social media icons
    "https://use.fontawesome.com/releases/v5.9.0/css/all.css",
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True


app.layout = build_desktop_layout


################################################################################
#
#    Register callbacks
#
################################################################################

register_routes_callbacks(app)   
register_desktop_callbacks(app)
register_desktop_callacks_data(app)


if __name__ == '__main__':
    app.run_server(debug=True)