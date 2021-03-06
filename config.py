import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'rbitra.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RBITRA_DECISION_PATH = os.path.join(basedir, "decisions")
    RBITRA_PLUGINS_PATH = os.path.join(basedir, "plugins")
