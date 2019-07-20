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
# import chart_studio.plotly as py
import plotly.tools as tls
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import pprint
# server = create_app()
# print(app.__name__)

mpl.use('agg')


def sample_plot():
    df_white = pd.read_csv(
        join(dirname(__file__), 'data', 'white.csv'), delimiter=';')
    df_corr = df_white.corr()
    mpl_fig = plt.figure()
    ax = mpl_fig.add_subplot(111)
    n=df_corr.shape[0]
    xs, ys=np.meshgrid(0.5+np.arange(n), 0.5+np.arange(n))
    xs,ys=xs.flatten(),ys.flatten()
    ax.scatter(xs,ys, s=20)
    mpl_fig
    # print(df_corr.shape)
    # print
    # plt.scatter(x, y, c=c,
    #                 s=np.square(s)*area_scale,
    #                 edgecolor=ec,
    #                 linewidth=ew*width_scale)
    # ax.grid()

    plotlyfig =  tls.mpl_to_plotly(mpl_fig)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(plotlyfig['layout'])
    return plotlyfig


def count_plot():
    mpl.use('agg')
    df_white = pd.read_csv(
        join(dirname(__file__), 'data', 'white.csv'), delimiter=';')
    df_red = pd.read_csv(
        join(dirname(__file__), 'data', 'red.csv'), delimiter=';')
    n_white, n_red = df_white.shape[0], df_red.shape[0]
    data_count = {'name': ['red', 'white'], 'count': [n_red, n_white]}
    # mpl_fig = plt.figure()
    # ax = mpl_fig.add_subplot(111)
    sns.barplot(x='name', y='count', data=data_count)
    return tls.mpl_to_plotly(plt.gcf())


def corr_plot():

    df_white = pd.read_csv(
        join(dirname(__file__), 'data', 'white.csv'), delimiter=';')
    df_corr = df_white.corr()
    mpl_fig = plt.figure()
    ax = mpl_fig.add_subplot(111)
    sns.heatmap(df_corr, ax=ax)
    # mpl_fig = plt.figure()
    # ax = mpl_fig.add_subplot(111)
    # ax.set_title('A Sine Curve')

    # n = len(df_corr.columns)
    # plt.yticks(np.arange(n), df_corr.columns[::-1])
    # plt.xticks(np.arange(n), df_corr.columns, rotation='vertical')
    # ax = plt.gca()
    # ax.xaxis.tick_top()
    # ax.set_aspect('equal')
    # plt.grid(False)
    # for i in range(n+1):
    #     plt.axvline(i-0.5, -0.5, n)
    #     plt.axhline(i-0.5, -0.5, n)
    # # plt.axvline()

    # cmap = mpl.colors.Colormap('mymap')
    # cmap.set_under("#2d3561")
    # cmap.set_over('#f3826f')
    # cmap = plt.get_cmap('viridis', 12)
    # scalable_map = mpl.cm.ScalarMappable(mpl.colors.Normalize(-1, 1), cmap)
    # patches = []
    # for i in (range(n)):
    #     for j in (range(n)):
    #         if i == j:
    #             continue
    #         v = df_corr.values[i, j]
    #         patches.append(Circle((i, n-j-1), abs(0.5*v), fc=cmap(v)))
    # # df_corr.values
    # ax.add_collection(PatchCollection(patches, match_original=True))
    # # plt.colorbar(scalable_map, ax=ax)
    # plt.ylim(-1, n)
    # plt.xlim(-1, n)
    return tls.mpl_to_plotly(mpl_fig)


def create_dash_app(app):
    dash_app = Dash(
        # app_name,
        server=app,
        routes_pathname_prefix='/dash/'
    )
    df = pd.read_csv(join(dirname(__file__), 'data', 'red.csv'), delimiter=';')
    n = df.columns.size

    xs, ys = np.meshgrid(np.arange(n), np.arange(n))
    xs, ys = xs.flatten(), ys.flatten()
    corr_matrix = df.corr().values[::-1, :]
    corr_values = corr_matrix.flatten()
    markers_size = abs(corr_values)
    fig_size = 800
    circle_size = 40
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
        width=fig_size, height=fig_size,
        yaxis=dict(
            dtick=30,
            scaleanchor="x", scaleratio=1,
            tickvals=np.arange(n),
            # ticktext=df.columns[::-1],
            showgrid=False,
            autorange=True
        ),
        xaxis=dict(
            showgrid=False,
            tickvals=np.arange(n), ticktext=df.columns, side='top',
            autorange=True,
        ),
        autosize=True,
        title='Correlation matrix',

    )

    dash_app.layout = html.Div(dcc.Graph(
        # figure=go.Figure(
        #     data=scatter,
        #     layout=layout
        # )
        # figure=count_plot(),
        # figure=corr_plot(),
        figure=sample_plot(),
    ))
