
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from os import path
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
red_df_path = path.join(path.dirname(
    path.abspath(__file__)), '..', 'data', 'red.csv')
white_df_path = path.join(path.dirname(
    path.abspath(__file__)), '..', 'data', 'red.csv')
df_red = pd.read_csv(red_df_path, delimiter=';')
df_white = pd.read_csv(white_df_path, delimiter=';')


def convert_class(x): return 'good' if x >= 7 else 'bad'


df_red['class'] = df_red['quality'].apply(convert_class)
df_white['class'] = df_white['quality'].apply(convert_class)

# path.
fig = px.histogram(df_white, x="alcohol",
                   color="class", opacity=0.5,
                   histnorm='probability density',
                   nbins=50,
                   )
fig.update_layout(barmode='overlay')
# fig.update_traces(opacity=0.5)
# fig.update_traces(marker={'opacity':0.5})
app.layout = html.Div(
    dcc.Graph(
        figure=fig,
        config={
            'displayModeBar': False
        }
    )
)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=80)
