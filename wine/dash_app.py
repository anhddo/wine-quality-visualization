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
from . import wine_app

LINK = dict(overview='/wine', explore='/wine/explore',
            classification='/wine/classification')


def get_red_df():
    return pd.read_csv(join(dirname(__file__), 'data', 'red.csv'), delimiter=';')


def get_white_df():
    return pd.read_csv(join(dirname(__file__), 'data', 'white.csv'), delimiter=';')


def correlation_graph():
    df = get_red_df()
    n = df.columns.size

    xs, ys = np.meshgrid(0.5+np.arange(n), 0.5+np.arange(n))
    xs, ys = xs.flatten(), ys.flatten()
    corr_matrix = df.corr().values[::-1, :]
    corr_values = corr_matrix.flatten()
    markers_size = abs(corr_values)
    fig_size = 900
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


def feature_histogram(feature_name):
    import plotly.figure_factory as ff
    df = get_red_df()
    def convert_class(x): return 'good' if x >= 7 else 'bad'
    df['class'] = df['quality'].apply(convert_class)
    d1 = df[df['class'] == 'bad'][feature_name]
    d2 = df[df['class'] == 'good'][feature_name]
    return dcc.Graph(
        figure=ff.create_distplot([d1, d2], ['bad', 'good'], bin_size=0.1)
    )


def feature_layout():
    df = get_red_df()
    return html.Div(children=[
        dcc.Dropdown(
            id='hist-dropdown',
            options=[{'label': e, 'value': e} for e in df.columns],
            value=df.columns[0]
        ),
        html.Div(id='hist-content')
    ])


def pie_chart():
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=1, cols=3,
                        specs=[
                            [{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]]
                        )
    red_df = get_red_df()
    white_df = get_white_df()
    def convert_class(x): return 'good' if x >= 7 else 'bad'
    white_df['class'] = white_df['quality'].apply(convert_class)
    good = (sum(white_df['class'] == 'good'))
    bad = white_df.shape[0]-good
    # red_df['class'] = df_red['quality'].apply(convert_class)
    fig.add_trace(go.Pie(
        labels=['Red white', 'White wine'],
        values=[red_df.shape[0], white_df.shape[0]],
        textinfo='value',
        hole=0.3
    ), row=1, col=1)

    fig.add_trace(go.Pie(
        labels=['good', 'bad'],
        values=[good, bad],
        hole=0.5
    ), row=1, col=2)
    red_df['class'] = red_df['quality'].apply(convert_class)
    good = (sum(red_df['class'] == 'good'))
    bad = red_df.shape[0]-good
    fig.add_trace(go.Pie(
        labels=['good', 'bad'],
        values=[good, bad],
        hole=0.5
    ), row=1, col=3)
    return dcc.Graph(
        figure=fig
    )


def preview_data():
    df = get_red_df().sample(frac=1).head(10)

    table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        style_data={'whiteSpace': 'normal'}
    )
    # print(table)
    return table


def layout():
    return html.Div(
        id='main-page',
        children=[
            dcc.Location(id='url', refresh=False),
            html.Div(
                'Group1: Dung Pham, Quan Hoang, Anh Do',
                className='group-info'
            ),
            html.Div(id='tab-bar', children=[
                dcc.Link('Overview', className='tab',
                         id='overview', href=LINK['overview']),
                dcc.Link('Explore', className='tab',
                         id='explore', href=LINK['explore']),
                dcc.Link('Classification', className='tab',
                         id='classification', href=LINK['classification']),
            ]),
            html.Div(id='page-content')
        ]
    )


def overview_layout():
    return html.Div([
        preview_data(),
        pie_chart()
    ])


def explore_layout():
    return html.Div([
        correlation_graph(),
        feature_layout()
    ])


def create_dash_app(app):
    dash_app = Dash(
        __name__,
        server=app,
        routes_pathname_prefix='/'
    )
    dash_app.config.suppress_callback_exceptions = True
    dash_app.layout = layout()
    @dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def update_url(pathname):
        if pathname == LINK['explore']:
            return explore_layout()
        elif pathname == LINK['overview']:
            return overview_layout()
        else:
            return preview_data()

    @dash_app.callback(Output('hist-content', 'children'), [Input('hist-dropdown', 'value')])
    def update_hist_graph(value):
        return feature_histogram(value)

    return dash_app
