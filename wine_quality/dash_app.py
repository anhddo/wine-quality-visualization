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

OPPOSITE_COLOR_0='crimson'
df_red = DF_RED.copy(deep=True)
df_white = DF_WHITE.copy(deep=True)
df_red['color'] = 'red'
df_white['color'] ='white'
df_combine = pd.concat([df_red, df_white])

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
        margin=dict(pad=0, t=0, l=0, r=0, b=0),
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


def correlation_graph():
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



def single_feature_red_white(feature_name):
    fig = ff.create_distplot(
        [DF_RED[feature_name], DF_WHITE[feature_name]],
        ['red wine', 'white wine'],
        bin_size=DF_RED[feature_name].std()/5,
        colors=[MAIN_COLOR_0, MAIN_COLOR_1],
        show_rug=False
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
        width=500, height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        #     paper_bgcolor="LightSteelBlue",
        plot_bgcolor="white",
    ))
    return fig


def feature_seperation_figure(feature_name, is_red=True):
    df = None
    if is_red:
        df = DF_RED.copy(deep=True)
    else:
        df = DF_WHITE.copy(deep=True)

    def convert_class(x): return 'good' if x >= 7 else 'bad'
    df['class'] = df['quality'].apply(convert_class)
    d1 = df[df['class'] == 'bad'][feature_name]
    d2 = df[df['class'] == 'good'][feature_name]
    fig = ff.create_distplot(
        [d1, d2], ['bad wine', 'good wine'], bin_size=df[feature_name].std() / 5,
        colors=[MAIN_COLOR_1, MAIN_COLOR_0], show_rug=False
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
        #     paper_bgcolor="LightSteelBlue",
        plot_bgcolor="white",
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
        children='''
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
        children=html.Div(
            children=[
                html.Div(
                    className='heading-1',
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
    return html.Div(
        className='board',
        children=[
            html.Div(
                className='heading-1',
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
            dcc.Loading(
                className='board',
                children=preview_dataframe(),
            ),
            simple_statistic_markdown(),
            dcc.Loading(
                className='d-flex flex-row',
                children=[
                    html.Div(
                        className='board d-flex',
                        children=count_chart()
                    ),
                    html.Div(
                        className='board d-flex',
                        children=pie_chart()
                    )
                ]
            )
        ])


def markdown_good_wine():
    return html.Div(
        className="board",
        children=[
            html.Div(className='heading-2', children='Correlation'),
            dcc.Markdown('''
                
                    * The dataset have 2 kind of wine. In the correlation matrix, upper triangle and lower triangle for red wine and white wine, respectively.  
                    * Look at the correlation matrix, alcohol have strong positive correlation in both wine type. That means increasing wine quality tend to increase the quality as well.
            ''')
        ]
    )


def question1():
    return html.Div(
        className='board',
        children=[
            html.Div(
                className='heading-1',
                children='1. What components make good wine?'
            ),
            dcc.Markdown(children='''
                * Wine score (from 0-10) is already given. Therefore, correlation value of the component value with wine score could determine which components make good wine. Features  having  strong  effect  onthe wine quality will have high absolute correlation score with the quality.  
                '''),

        ]
    )


def question2():
    return html.Div(
        className='board',
        children=[
            html.Div(className='heading-1', children='''
                2. Is there any relations between components, explain those relations?
                '''),
            dcc.Markdown('''
                        Alcohol and density pair have very strong negative correlation score, especially in white wine. Due to common knowledge, the density of ethanol is $0.789 g/cm^3$ and the density water is $1.000 g/cm^3$.  Intuitively, increasing alcohol will lower the density of wine.
                    ''')
        ]
    )


def correlation_section(**kargs):
    return html.Div(
        className='d-flex',
        children=[
            markdown_good_wine(),
            html.Div(
                id='correlation-graph',
                className='board d-flex',
                children=[
                    correlation_graph(**kargs),
                ]
            ),
        ]
    )


def good_feature_section():
    return html.Div(
        className='d-flex',
        children=[
            html.Div(className='board', children=[
                html.Div(className='heading-2', children='Good feature!'),
                dcc.Markdown('''
                Histogram is a good visualization which show the separation strength of each components. Thus, good feature are features that separate clearly good and bad wine.
                ''')
            ]),
            html.Div(
                # color=MAIN_COLOR_0,
                children=dcc.Loading(
                    className='board',
                    children=[
                        dcc.Dropdown(
                            id='hist-dropdown',
                            options=[{'label': e, 'value': e}
                                     for e in DF_RED.columns],
                            value='alcohol'
                        ),
                        dcc.Graph(
                            id='hist-graph'
                        )
                    ]
                )
            )
        ]
    )


def question3():
    return html.Div(
        className='board',
        children=[
            html.Div(className='heading-1',
                     children='3. Does red wine and white wine share the same quality criteria?'),
            dcc.Markdown('''
                * Both kind of wine share the same criteria on the alcohol. It seem the higher level of alcohol the better.
                * However, two wine type have different criteria in density and volatile acidity. 
                * In general, people prefer low density wine, especially in white wine. That make sense cause people also prefer high level of alcohol.
                * Low volatile acidity is important for red wine, but it's not so important for the white one. As the name suggests, volatile acidity (VA) is referencing volatility in wine, which causes it to go bad. Acetic acid builds up in wine when there’s too much exposure to oxygen during winemaking and is usually caused by acetobacter (the vinegar-making bacteria!). Volatile acidity is considered a fault at higher levels (1.4 g/L in red and 1.2 g/L in white) and can smell sharp like nail polish remover.
            ''')
        ]
    )


def single_feature_section():
    return html.Div(
        className='d-flex flex-row',
        children=[
            html.Div(
                className='board',
                children=[
                    html.Div(
                        className='heading-2',
                        children="Single feature"
                    ),
                    dcc.Markdown(children='''
                        Histogram is very good to find resonable good feature to discriminate wine color, such as: " **volatile acidity**", "**total sulfur dioxide**".
                    '''),
                ]
            ),
            html.Div(
                className='board',
                children=[
                    dcc.Dropdown(
                        id='color-dropdown',
                        options=[{'label': e, 'value': e}
                                 for e in DF_RED.columns],
                        value='total sulfur dioxide'
                    ),
                    dcc.Loading(
                        dcc.Graph(
                            id='single-ftr-hist',
                        )
                    )

                ]
            )
        ]
    )


def pair_feature_section():
    return html.Div(
        # className='d-flex flex-row',
        children=[
            html.Div(
                className='board',
                children=[
                    html.Div(
                        className='heading-2',
                        children="Pair features"
                    ),
                    dcc.Markdown(children='''
                        With one more attribute, the separation is a bit clearer using scatter plot or density contour plot.  
                        **Pair features give good separation:**
                        * total sulfur dioxide, chlorides
                        * sulphates, chlorides
                        * sulphates, fixed acidity
                    '''),
                ]
            ),
            html.Div(
                className='board',
                children=[
                    html.Div(
                        className='row justify-content-center',
                        children=[
                            html.Div(
                                className='w-25 mr-3',
                                children=dcc.Dropdown(
                                    id='1st-ftr-dropdown',
                                    options=[{'label': e, 'value': e}
                                             for e in DF_RED.columns],
                                    value='total sulfur dioxide'
                                ),
                            ),
                            html.Div(
                                className='w-25',
                                children=dcc.Dropdown(
                                    id='2nd-ftr-dropdown',
                                    options=[{'label': e, 'value': e}
                                             for e in DF_RED.columns],
                                    value=DF_RED.columns[2]
                                ),
                            )
                        ]
                    ),
                    dcc.Loading(
                        html.Div(
                            className='d-flex',
                            children=[
                                dcc.Graph(
                                    id='pair-scatter-graph',
                                ),
                                dcc.Graph(
                                    id='pair-contour-graph'
                                )
                            ]
                        )
                    )

                ]
            )
        ]
    )

def pair_scatter(ftr0, ftr1):
    fig = px.scatter(df_combine, x=ftr0, y=ftr1,
                color='color', 
                color_discrete_sequence=[OPPOSITE_COLOR_0, MAIN_COLOR_0],
                opacity=0.3
    )
    fig.update_layout(dict(
        width=400, height=400, legend=dict(xanchor='left', x=0, y=1.2),
        margin=dict(l=0, r=0)
    ))
    return fig

def pair_contour(ftr0, ftr1):
    fig = px.density_contour(
        df_combine, x=ftr0, y=ftr1, color="color", 
        color_discrete_sequence=[OPPOSITE_COLOR_0, MAIN_COLOR_0],
        marginal_x="histogram", marginal_y="histogram"
    )

    fig.update_layout(dict(
        width=500, height=400, legend=dict(xanchor='left', x=0, y=1.2),
        margin=dict(l=0, r=0)
    ))
    return fig

def question4():
    return html.Div(
        className='',
        children=[
            html.Div(
                className='board',
                children=html.Div(
                    className='heading-1',
                    children='4. Which component differ white wine and red wine?'
                ),
            ),
            # single_feature_section(),
            pair_feature_section()
        ]
    )


def explore_content():
    return [
        question1(),
        correlation_section(),
        good_feature_section(),
        question2(),
        question3(),
        question4(),
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
            return explore_layout()
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
        return feature_seperation_figure(value)


def color_dropdown_callback(dash_app):
    @dash_app.callback(Output('single-ftr-hist', 'figure'), [Input('color-dropdown', 'value')])
    def update_hist_graph(value):
        return single_feature_red_white(value)


def pair_dropdown_callback(dash_app):
    @dash_app.callback(
        [Output('pair-scatter-graph', 'figure'), Output('pair-contour-graph', 'figure')],
        [Input('1st-ftr-dropdown', 'value'), Input('2nd-ftr-dropdown', 'value')]
    )
    def func(first, second):
        return (pair_scatter(first, second), pair_contour(first, second))


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
    pair_dropdown_callback(dash_app)
    return dash_app
