from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()


# app context (see flask-sqlalchemy contexts)
app = Flask(__name__)
def create_app(*,test=False):
    if test is True:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
    else:
        app.config.from_object(Config)
        db.init_app(app)
    return app


from rbitra import api, models
