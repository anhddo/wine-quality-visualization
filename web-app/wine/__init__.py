import flask
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from flask import Blueprint, render_template
from dash.dependencies import Input, Output
import time
import os

server = flask.Flask(__name__)

# bp = Blueprint('auth', __name__, url_prefix='/auth')
@server.route('/')
def index():
    return render_template('index.html')


app = dash.Dash(
    server=server,
    routes_pathname_prefix='/dash/'
)

loading_screen = dash.Dash(server=server, routes_pathname_prefix='/loading/')
loading_screen.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1('Loading data'),
    dcc.Loading(id="loading-1",
                children=[html.Div(id="loading-output-1")],
                type="default")
])
app.layout = html.Div(
    children=[
        html.H3("Edit text input to see loading state"),
        dcc.Input(id="input-1", value='Input triggers local spinner'),
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='MTL'
        )
    ]
)


@loading_screen.callback(Output('url', 'pathname'), [Input("loading-1", "children")])
def to_main(value):
    print('============')
    print(57, value)
    print('============')
    if value == None:
        return '/'
    return '/main'


@loading_screen.callback(Output("loading-output-1", "children"), [
    Input('url', 'pathname')
])
def input_triggers_spinner(value):
    print('er hererererer')
    # df=pd.read_csv('../data/white.csv')
    time.sleep(3)
    return ""


# print(200, os.path.abspath(os.curdir))
if __name__ == '__main__':
    # app.run_server(debug=True)
    server.run()
