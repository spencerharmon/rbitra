import os

basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig(object):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RBITRA_DECISION_PATH = os.path.join(basedir, "rbitra", "decisions")
    RBITRA_PLUGINS_PATH = os.path.join(basedir, "testplugins")
