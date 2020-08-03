import dash_html_components as html
from dash.dependencies import Input, Output, State

import sys
sys.path.append('../')
from layout import  navbar, desktop_body
from utils import StatesDataFrame



def register_routes_callbacks(app):
    

    @app.callback(
        [Output("page-content", "children")],
        [Input("url", "pathname")]
    )  
    def display_page(pathname):
        if pathname == '/':
            return [desktop_body]
        else:
            return [desktop_body]
      