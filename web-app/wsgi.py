from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from main import app as flask_app
from wine_hist import app as dash_app
from app2 import app as dash_app2
dash_app.enable_dev_tools(debug=True)  
application = DispatcherMiddleware(flask_app, {
    '/app1': dash_app.server,
    '/app2': dash_app2.server,
})  
if __name__ == '__main__':
    run_simple('localhost', 8050, application)  