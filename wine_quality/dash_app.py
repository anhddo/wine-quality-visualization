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
import plotly.figure_factory as ff
import dash_table
import matplotlib.pyplot as plt
import plotly.tools as tls
import matplotlib as mpl
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import pprint
from . import wine_app
import time

LINK = dict(overview='/wine', explore='/wine/explore',
            classification='/wine/classification',
            about='/wine/about')
RED0 = '#820505'
WHITE0 = '#e8e1e1'


def load(file_name):
    print('Load ' + file_name)
    return pd.read_csv(join(dirname(__file__), 'data', file_name), delimiter=';')


DF_RED = load('red.csv')
DF_WHITE = load('white.csv')


def correlation_graph():
    df = DF_RED
    corr_matrix = df.corr().values  # [::-1, :]
    n = df.columns.size
    M = []
    for row in range(n):
        for col in range(n):
            if row != col:
                M.append((0.5+col, 0.5+n-1-row, corr_matrix[row, col]))
    xs, ys, corr_values = zip(*M)
    markers_size = abs(np.array(corr_values))
    fig_size = 500
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
            colorscale=[
                [0, '#4a4142'],
                [1, RED0]
            ]
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
    for row in range(n+1):
        fig.add_scatter(x=[0, n], y=[row, row], mode='lines',
                        marker=dict(color='white'))
        fig.add_scatter(x=[row, row], y=[0, n], mode='lines',
                        marker=dict(color='white'))
    # print(type(fig['data']))
    # import sys
    # print(sys.getsizeof(fig['data']), sys.getsizeof(df))
    return dcc.Graph(
        id='correlation',
        figure=fig,
        config=dict(displayModeBar=False),
        style={'display': 'inline-block'}
    )


def color_hist(feature_name):
    df_white = DF_WHITE.copy(deep=True)
    df_red = DF_RED.copy(deep=True)
    df_white['type'] = 'white'
    df_red['type'] = 'red'
    df = pd.concat([df_red, df_white], ignore_index=True)
    d1 = df[df['type'] == 'white'][feature_name]
    d2 = df[df['type'] == 'red'][feature_name]
    fig = ff.create_distplot(
        [d1, d2], ['white wine', 'red wine'], colors=[WHITE0, RED0])
    fig.update_layout(dict(width=500))
    return dcc.Graph(
        figure=fig
    )


def feature_histogram(feature_name):
    df = DF_RED.copy(deep=True)
    def convert_class(x): return 'good' if x >= 7 else 'bad'
    df['class'] = df['quality'].apply(convert_class)
    d1 = df[df['class'] == 'bad'][feature_name]
    d2 = df[df['class'] == 'good'][feature_name]
    fig = ff.create_distplot(
        [d1, d2], ['bad wine', 'good wine'], bin_size=0.1, colors=[WHITE0, RED0]
    )
    fig.update_traces(
        marker=dict(
            line=dict(
                width=1,
                color='black'
            )
        ),
    )

    fig.update_layout(dict(
        width=500,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        plot_bgcolor="LightSteelBlue",
    ))
    return fig


def feature_layout():
    df = DF_RED
    return html.Div(
        style={'width': '500px', 'display': 'inline-block'},
        children=[
            dcc.Loading(color=RED0, children=[
                dcc.Dropdown(
                    id='hist-dropdown',
                    options=[{'label': e, 'value': e} for e in df.columns],
                    value='alcohol'
                ),
                dcc.Graph(
                    id='hist-graph'
                )

            ])
        ])


def pie_chart():
    from plotly.subplots import make_subplots

    red_df = DF_RED.copy(deep=True)
    white_df = DF_WHITE.copy(deep=True)
    def convert_class(x): return 'good' if x >= 7 else 'bad'
    white_df['class'] = white_df['quality'].apply(convert_class)
    good = (sum(white_df['class'] == 'good'))
    bad = white_df.shape[0]-good
    bar_fig = go.Figure(layout=go.Layout(width=450))
    bar_fig.add_trace(go.Bar(
        x=['Red white', 'White wine'],
        y=[red_df.shape[0], white_df.shape[0]],
        marker_color=[RED0, WHITE0]
    ))

    fig = make_subplots(
        rows=1, cols=2,
        specs=[
            [{'type': 'pie'}, {'type': 'pie'}]
        ],
        subplot_titles=("White Wine", "Red Wine")
    )
    fig.update_layout(dict(width=600))

    fig.add_trace(go.Pie(
        labels=['good', 'bad'],
        values=[good, bad],
        marker=dict(colors=[RED0, WHITE0]),
        hole=0.5
    ), row=1, col=1)

    red_df['class'] = red_df['quality'].apply(convert_class)
    good = (sum(red_df['class'] == 'good'))
    bad = red_df.shape[0]-good
    fig.add_trace(go.Pie(
        labels=['good', 'bad'],
        values=[good, bad],
        marker=dict(colors=[RED0, WHITE0]),
        hole=0.5
    ), row=1, col=2)
    return html.Div(
        children=[
            dcc.Graph(
                figure=bar_fig,
                style={'display': 'inline-block'}
            ),
            dcc.Graph(
                figure=fig,
                style={'display': 'inline-block'}
            )

        ],
        style={'display': 'inline-block'}
    )


def preview_data():
    df = DF_RED.sample(frac=1).head(10)

    table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_header={'backgroundColor': RED0, 'color': 'white'},
        style_data={'border': '1px solid ' + RED0},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': WHITE0,
            }
        ]
    )
    # print(table)
    return table


def create_tab(str, id, href):
    return html.Div(
        className='tab',
        children=[
            dcc.Link(str, href=href),
        ]

    )


def layout():
    return html.Div(
        id='main-page',
        children=[
            dcc.Location(id='url', refresh=False),
            html.Div(
                'Visual Analytics',
                id='subject'
            ),
            html.Div(
                'Wine Quality',
                id='header'
            ),
            html.Div(id='tab-bar', children=[
                create_tab('Dataset', 'overview', LINK['overview']),
                create_tab('Explore data', 'explore', LINK['explore']),
                create_tab('Classification', 'classification',
                           LINK['classification']),
                create_tab('About', 'about', LINK['about']),
            ]),
            dcc.Loading(
                color=RED0,
                children=[
                    html.Div(id='page-content')
                ],

                type="default"
            )
        ]
    )


def overview_layout():
    return html.Div([
        preview_data(),
        pie_chart()
    ])


def explore_layout():
    return html.Div(
        [
            html.Div(
                id='good-wine-explain',
                className='shadow-block',
                children=[
                    html.Div('What components make good wine?'),
                    html.Div('Is there any relations between components?'),
                    # correlation_graph(),
                    # feature_layout(),
                ]
            ),
            html.Div(
                id='color-section',
                className='shadow-block',
                children=[
                    html.Div(
                        'Is there any components which differ red wine and white wine?', className='left'
                    ),
                    html.Div(className='right',
                             children=color_hist('total sulfur dioxide')
                             ),

                ]),
            html.Div(
                'Does red wine and white wine share the same quality criteria?'
            )
        ]
    )


def create_dash_app(app):
    dash_app = Dash(
        __name__,
        server=app,
        routes_pathname_prefix='/'
    )
    dash_app.config.suppress_callback_exceptions = True
    dash_app.title = 'Wine Quality'
    dash_app.layout = layout()
    @dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def update_url(pathname):
        if pathname == LINK['explore']:
            return explore_layout()
        elif pathname == LINK['overview']:
            return overview_layout()
        elif pathname == LINK['about']:
            return html.Div(
                'Group1: Dung Pham, Quan Hoang, Anh Do',
                id='about',
                style={'text-align': 'center'}
            )
        else:
            return html.Div("nothing yet")

    @dash_app.callback(Output('hist-graph', 'figure'), [Input('hist-dropdown', 'value')])
    def update_hist_graph(value):
        return feature_histogram(value)

    return dash_app
