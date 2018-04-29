from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_apiexceptions import JSONExceptionHandler, ApiException, api_exception_handler


app = Flask(__name__)

db = SQLAlchemy()

# app context (see flask-sqlalchemy contexts)
def create_app(*,test=False):
    if test is True:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)
    return app


from rbitra import api, models
