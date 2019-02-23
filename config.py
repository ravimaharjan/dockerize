import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    # environment or hardcoded key is not the good way to store secret_key. 
    # research more where to store it or how. 
    SECRET_KEY = "mroF#01$ksalF!"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False