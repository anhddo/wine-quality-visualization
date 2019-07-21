from wine import wine_app
from wine.dash_app import create_dash_app
# app = create_dash_app(wine_app.create_app()).server
app = create_dash_app(wine_app.create_app()).server

# if __name__ == "__main__":
#     app.run_server(debug=True)