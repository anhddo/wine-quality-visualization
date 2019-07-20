from wine.app import create_app
# from wine.dash_app import dash_app
import dash_html_components as html
from dash import Dash
from flask import 
dash_app = Dash(__name__,
                requests_pathname_prefix='/')
dash_app.layout = html.Div('hello world')
if __name__ == "__main__":
    # app = create_app()
    # app.run(port=8050, debug=True)
    print("asdad")
    dash_app.run_server(debug=True)

