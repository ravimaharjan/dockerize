from flask import Flask
from db_provider import db
from config import Config
from webapp.applications.home import home_app
from webapp.applications.user import user_app
from extensions import login_manager
from flask_login import LoginManager
from database.dbconnection import get_connection
import logging as log
# app = Flask(__name__)

# @app.route("/")
# def index():
#     log.warn("index called")

#     return """
#     <h1>Python Flask in Docker!</h1>
#     <p>A sample web-app for running Flask inside Docker.</p>
#     """

def create_app(config_file):
    log.warn("create_app called")
    app = Flask(__name__)
    # from webapp import models
    
    app.config.from_object(Config)
    register_blueprint(app)
    register_extensions(app)
    log.warn(app)
    return app

def register_blueprint(app):
    app.register_blueprint(home_app)
    app.register_blueprint(user_app)

def register_extensions(app):
    # db.init_app(app)
    log.warn(get_connection("mongodb://mongo:27017", 27017))
    # migrate.init_app(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user_app.login"

app = create_app("")

# if __name__ == "__main__":

#     app = create_app("")
#     log.warn("main method")
#     # app.run(debug=True, host="0.0.0.0", port=5000)
#     app.run("0.0.0.0", debug=True, port=5000)

