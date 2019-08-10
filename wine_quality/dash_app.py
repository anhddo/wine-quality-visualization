import numpy as np
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
from plotly.subplots import make_subplots
import dash_table
import plotly.tools as tls
import pprint
import time

LINK = dict(overview='/', explore='/wine/explore',
            classification='/wine/classification',
            about='/wine/about')
MAIN_COLOR_0 = 'dodgerblue'
MAIN_COLOR_1 = 'lightskyblue'
WHITE0 = '#e8e1e1'


def load(file_name):
    print('Load ' + file_name)
    return pd.read_csv(join(dirname(__file__), 'data', file_name), delimiter=';')


DF_RED = load('red.csv')
DF_WHITE = load('white.csv')


def correlation_fig(**kargs):
    cscale = [[0, 'black'], [1, MAIN_COLOR_0]]
    fig_size = 600
    circle_size = fig_size/20.0
    n = DF_RED.shape[1]

    def create_scatter(name, M, circle_size, **kargs_marker):
        xs, ys, corr_values = zip(*M)
        markers_size = abs(np.array(corr_values))
        return go.Scatter(
            name=name,
            x=xs,
            y=ys,
            mode='markers',
            hovertext=corr_values,
            showlegend=True,
            marker=dict(
                size=markers_size * circle_size,
                cmax=1,
                cmin=-1,
                color=corr_values,
                colorscale=cscale,
                **kargs_marker
            )
        )

    shared_axes_conf = dict(
        showgrid=False,
        tickvals=0.5+np.arange(n),
        ticktext=DF_RED.columns,
        zeroline=False
    )

    xaxis_conf = dict(
        side='top',
        range=[-0.5, 12.5],
        tickangle=-90,
        **shared_axes_conf
    )

    yaxis_conf = dict(
        scaleanchor="x",
        scaleratio=1,
        autorange='reversed',
        range=[0, 11],
        **shared_axes_conf
    )

    layout = go.Layout(
        yaxis=yaxis_conf,
        xaxis=xaxis_conf,
        #     showlegend=False,
        width=fig_size, height=fig_size,
        margin=dict(pad=0),
        plot_bgcolor="white"
    )

    corr_red = DF_RED.corr().values
    corr_red = [(0.5 + col, 0.5 + row, corr_red[row, col])
                for row in range(n) for col in range(n) if row != col and col > row]

    corr_white = DF_WHITE.corr().values
    corr_white = [(0.5 + col, 0.5 + row, corr_white[row, col])
                  for row in range(n) for col in range(n) if row != col and col < row]
    data = [
        create_scatter('Red wine', corr_red, circle_size, symbol='circle'),
        create_scatter('White wine', corr_white,
                       circle_size, symbol='star-square')
    ]

    line_settings = dict(mode='lines', line=dict(width=1),
                         marker=dict(color='black'), showlegend=False)
    for row in range(n+1):
        data.append(go.Scatter(x=[0, n], y=[row, row], **line_settings))
        data.append(go.Scatter(x=[row, row], y=[0, n], **line_settings))
    data.append(go.Scatter(x=[0, n], y=[0, n], **line_settings))
    fig = go.Figure(
        data=data,
        layout=layout
    )
    return fig


def correlation_graph(**kargs):

    # fig.add_trace(correlation_fig(wine_type='red'), row=1,col=1)
    # fig.add_trace(correlation_fig(wine_type='white'), row=1, col=2)
    # print(type(fig['data']))
    # import sys
    # print(sys.getsizeof(fig['data']), sys.getsizeof(df))
    return dcc.Loading(
        children=[
            dcc.Graph(
                # id='correlation-white',
                figure=correlation_fig(wine_type='white'),
                config=dict(displayModeBar=False),
                style={'display': 'inline-block', 'overflow': 'auto'}
            )
        ],


        color=MAIN_COLOR_0
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
        [d1, d2], ['white wine', 'red wine'], colors=[WHITE0, MAIN_COLOR_0])
    fig.update_layout(dict(width=500))
    return fig


def feature_histogram(feature_name):
    df = DF_RED.copy(deep=True)
    def convert_class(x): return 'good' if x >= 7 else 'bad'
    df['class'] = df['quality'].apply(convert_class)
    d1 = df[df['class'] == 'bad'][feature_name]
    d2 = df[df['class'] == 'good'][feature_name]
    fig = ff.create_distplot(
        [d1, d2], ['bad wine', 'good wine'], bin_size=0.1, colors=[WHITE0, MAIN_COLOR_0]
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
            dcc.Loading(color=MAIN_COLOR_0, children=[
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


def count_chart():
    color = [MAIN_COLOR_0, MAIN_COLOR_1]

    bar_fig = go.Figure(
        layout=go.Layout(
            width=300,
            margin=dict(
                t=0, l=0, r=0, b=0
            )
        )
    )

    bar_fig.add_trace(go.Bar(
        x=['Red white', 'White wine'],
        y=[DF_RED.shape[0], DF_WHITE.shape[0]],
        marker_color=color
    ))
    return dcc.Graph(figure=bar_fig)


def pie_chart():
    color = [MAIN_COLOR_0, MAIN_COLOR_1]
    def count_good(df): return sum(df.quality >= 7)
    def count_bad(df): return df.shape[0] - count_good(df)
    # color = ['steelblue', 'powderblue']
    fig = make_subplots(
        rows=1, cols=2,
        specs=[
            [{'type': 'pie'}, {'type': 'pie'}]
        ],
        subplot_titles=("Red Wine", "White Wine")
    )

    pie_settings = dict(
        name='', labels=['good', 'bad'], marker=dict(colors=color), hole=0.5)
    fig.add_trace(go.Pie(
        values=[count_good(DF_RED), count_bad(DF_RED)],
        **pie_settings
    ), row=1, col=1)

    fig.add_trace(go.Pie(
        values=[count_good(DF_WHITE), count_bad(DF_WHITE)],
        **pie_settings
    ), row=1, col=2)
    fig.update_layout(
        margin=dict(
            t=20, l=0, r=0, b=0
        ),
        width=500
    )
    return dcc.Graph(figure=fig)


def preview_dataframe():
    rowEvenColor = 'deepskyblue'
    rowOddColor = 'dodgerblue'

    rowEvenColor = 'deepskyblue'
    rowOddColor = 'steelblue'
    rowOddColor = 'dodgerblue'

    df = DF_RED.head(10)
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=df.columns,
                    line_color='black',
                    fill_color='dodgerblue',
                    font_color='white',
                    font_size=12,
                    align='center'
                ),
                cells=dict(
                    values=df.values.T,  # 2nd column
                    line_color='black',
                    #                fill_color='white',
                    fill_color=[['white', 'lightgray']*5],
                    font_color='black',
                    align='center')
            )
        ],
        layout=dict(
            #         title=dict(
            #             text='Dataset sample',
            #             x=0.5,
            #             y=0.2
            # #             xanchor='center'
            #         ),
            margin=dict(t=0, l=0, r=0, b=0)
        )
    )

    return dcc.Graph(figure=fig)


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
                # create_tab('Classification', 'classification', LINK['classification']),
                create_tab('About', 'about', LINK['about']),
            ]),
            dcc.Loading(
                color=MAIN_COLOR_0,
                children=[

                    html.Div(id='page-content')
                ],

                type="default"
            )
        ]
    )

def about_markdown():
    return dcc.Markdown(
        className='board',
        children=
        '''
        **John von Neumann Institute ICT 2018**  
        **Group 1:**
        * Pham Tien Dung
        * Hoang Hong Quan
        * Do Duc Anh

        **Stack:**
        * Dash
        * Flask
        * Bootstrap
        * Python libraries: numpy, pandas
        '''

    )

def introduction():
    return html.Div(
        className='board',
        children=
            html.Div(
                children=[
                    html.Div(
                        className='heading',
                        children='Introduction'
                    ),

                    dcc.Markdown(
                        '''
                        The two datasets are red and white wine of the ** Portuguese "Vinho Verde" ** wine. 
                        The inputs include based onsensory data and the output is evaluated by experts.  
                        Each expert graded the wine quality between 0 (very bad)and 10 (excellent).  The quality is the median of at least 3 evaluations made by wine expert.  
                        '''
                    )
                ]
            )
        
    )

def simple_statistic_markdown():
    return  html.Div(
        className='board',
        children=[
            html.Div(
                className='heading',
                children='Statistic'
            ),
            dcc.Markdown(
                children='''
                The samples of white wine tripple the samples of red wine. To make classification simple, any sample having quality score greater than 7 will be assigned to good wine, less than 7 is bad wine. In general, the good wine percentage of white wine is bigger than the red one, 21.6% and 13%, respectively.
                '''
            ),
        ]
    )

def overview_layout():
    return html.Div(
        # className='board',
        children=[
            introduction(),
            html.Div(
                className='board',
                children=preview_dataframe(),
            ),
            simple_statistic_markdown(),
            html.Div(
                className='d-flex flex-row',
                children=[
                    html.Div(
                        className='board',
                        children=count_chart()
                    ),
                    html.Div(
                        className='board',
                        children=pie_chart()
                    )
                ]
            )
        ])


def markdown_good_wine():
    return html.Div(className="board", children=[
        dcc.Markdown('''
               
                * The dataset have 2 kind of wine. In the correlation matrix, upper triangle and lower triangle for red wine and white wine, respectively.  
                * Look at the correlation matrix, alcohol have strong positive correlation in both wine type. That means increasing wine qualitytend to increase the quality as well.
        ''')
    ])


def explore_content(**kargs):
    return [
        html.Div(children=[
            dcc.Markdown(className='board', children='''
            ## What components make good wine?
            * Wine score (from 0-10) is already given. Therefore, correlation value of the component value with wine score could determine which components make good wine. Features  having  strong  effect  onthe wine quality will have high absolute correlation score with the quality.  
            '''),
            html.Div(className='d-flex', children=[
                markdown_good_wine(),
                html.Div(
                    id='good-wine-explain',
                    className='board',
                    children=[
                        correlation_graph(**kargs),
                    ]
                ),
            ]),
            html.Div(
                className='d-flex',
                children=[

                ]
            )
        ]),
        html.Div(
            id='color-section',
            className='board',
            children=[
                html.Div(
                    'Is there any components which differ red wine and white wine?', className='left'
                ),
                dcc.Loading(
                    color=MAIN_COLOR_0,
                    children=html.Div(
                        className='right',
                        children=[
                            dcc.Dropdown(
                                id='color-dropdown',
                                options=[{'label': e, 'value': e}
                                         for e in DF_RED.columns],
                                value='total sulfur dioxide'
                            ),
                            dcc.Graph(
                                id='color-hist-graph',
                                figure=color_hist('total sulfur dioxide')
                            )
                        ]
                    ),
                )

            ]),
        html.Div(
            'Does red wine and white wine share the same quality criteria?'
        )
    ]


def explore_layout(**kargs):
    return html.Div(
        children=[
            dcc.Loading(
                children=html.Div(
                    id='explore-content',
                    children=explore_content(**kargs)
                ),
                color=MAIN_COLOR_0
            )
        ]
    )


def page_content_callback(dash_app):
    @dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def update_url(pathname):
        if pathname == LINK['explore']:
            return explore_layout(wine_type='red')
        elif pathname == LINK['overview']:
            return overview_layout()
        elif pathname == LINK['about']:
            return about_markdown()
        else:
            return html.Div("nothing yet")


def choose_wine_callback(dash_app):
    @dash_app.callback(Output('correlation', 'figure'), [Input('select-wine', 'value')])
    def func(value):
        return correlation_fig(wine_type=value)


def hist_graph_dropdown_callback(dash_app):
    @dash_app.callback(Output('hist-graph', 'figure'), [Input('hist-dropdown', 'value')])
    def update_hist_graph(value):
        return feature_histogram(value)


def color_dropdown_callback(dash_app):
    @dash_app.callback(Output('color-hist-graph', 'figure'), [Input('color-dropdown', 'value')])
    def update_hist_graph(value):
        return color_hist(value)


def register_dash(app):
    # <link rel="stylesheet"
    # crossorigin="anonymous">
    external_stylesheets = [
        {
            'href': "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
            'rel': 'stylesheet',
            'integrity': "sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
            'crossorigin': 'anonymous'
        }
    ]
    external_scripts = [
        {
            'href': "https://code.jquery.com/jquery-3.3.1.slim.min.js",
            'integrity': "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
            'crossorigin': "anonymous"
        },
        {
            'href': "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",
            'integrity': "sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM",
            'crossorigin': "anonymous"
        }
    ]

    dash_app = Dash(
        __name__,
        server=app,
        routes_pathname_prefix='/',
        external_scripts=external_scripts,
        external_stylesheets=external_stylesheets
    )
    dash_app.config.suppress_callback_exceptions = True
    dash_app.title = 'Wine Quality'
    dash_app.layout = layout()

    choose_wine_callback(dash_app)
    page_content_callback(dash_app)
    hist_graph_dropdown_callback(dash_app)
    color_dropdown_callback(dash_app)
    return dash_app
