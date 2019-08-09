import flask
import dash
import dash_html_components as html
from .dash_app import register_dash

app = flask.Flask(__name__)
dash_app = register_dash(app)