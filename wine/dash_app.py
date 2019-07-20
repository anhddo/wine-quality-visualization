import numpy as np
import seaborn as sns
import plotly.express as px
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import os
from os.path import join, dirname
import pandas as pd
import plotly.graph_objects as go
import dash_table
import plotly.tools as tls
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import pprint

def get_red_df():
    return pd.read_csv(join(dirname(__file__), 'data', 'red.csv'), delimiter=';')

def correlation_graph():
    df=get_red_df()
    n = df.columns.size

    xs, ys = np.meshgrid(0.5+np.arange(n), 0.5+np.arange(n))
    xs, ys = xs.flatten(), ys.flatten()
    corr_matrix = df.corr().values[::-1, :]
    corr_values = corr_matrix.flatten()
    markers_size = abs(corr_values)
    fig_size = 800
    circle_size = fig_size/20.0
    scatter = go.Scatter(
        x=xs, y=ys, mode='markers',
        hovertext=corr_values,
        marker=dict(
            size=markers_size * circle_size,
            cmax=1,
            cmin=-1,
            color=corr_values,
            colorbar=dict(
                title="Colorbar"
            ),
            colorscale="Viridis"
        )
    )

    layout = go.Layout(
        showlegend=False,
        width=fig_size, height=fig_size,
        margin=dict(pad=0),
        yaxis=dict(
            scaleanchor="x", scaleratio=1,
            tickvals=0.5+np.arange(n),
            ticktext=df.columns[::-1],
            showgrid=False,
            autorange=False,
            range=[0, 11],
            zeroline=False
        ),
        xaxis=dict(
            showgrid=False,
            tickvals=0.5+np.arange(n),
            ticktext=df.columns,
            side='top',
            range=[-0.5, 12.5],
            autorange=False,
            zeroline=False
        ),
        # autosize=True,
        # title='Correlation matrix',

    )
    fig = go.Figure(
        data=scatter,
        layout=layout
    )
    for i in range(n+1):
        fig.add_scatter(x=[0, n], y=[i, i], mode='lines',
                        marker=dict(color='white'))
        fig.add_scatter(x=[i, i], y=[0, n], mode='lines',
                        marker=dict(color='white'))
    return dcc.Graph(
        figure=fig,
        config=dict(displayModeBar=False)
    )

def preview_data():
    df=get_red_df().sample(frac=1).head(10)
    
    table= dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )
    # print(table)
    return table


def overview_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div('Group1: Pham Tien Dung, Hoang Hong Quan, Do Duc Anh'),
        dcc.Link('Overview', id='overview', href='/wine'),
        html.Br(),
        dcc.Link('Explore', id='explore', href='/explore'),
        html.Div(id='page-content', children=[preview_data()])
    ])


def explore_layout():
    return html.Div([
        correlation_graph()
    ])


def create_dash_app(app):
    dash_app = Dash(
        server=app,
        routes_pathname_prefix='/wine/'
    )

    dash_app.layout = overview_layout()
    @dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def update_url(pathname):
        print(pathname)
        if pathname == '/explore':
            return explore_layout()
        elif pathname=='/wine':
            return preview_data()
        else:
            return preview_data()
