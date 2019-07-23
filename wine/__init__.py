import flask
import dash
import dash_html_components as html
# from .app import create_app
# from . import dash_app
from . import wine_app
from . import dash_app

def create_app():
    app = wine_app.create_app()
    dash_app.create_dash_app(app)
    return app