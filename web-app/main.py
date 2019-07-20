from flask import Flask
from werkzeug.debug import DebuggedApplication
app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

asdasdasd
if __name__ == "__main__":
    app.run(host='0.0.0.0')
