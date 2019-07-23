from wine_quality import wine_app
from wine_quality.dash_app import create_dash_app
dash_app = create_dash_app(wine_app.create_app())
app = dash_app.server
if __name__ == "__main__":
    dash_app.run_server(debug=True)
