import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Warning: the Numeric date type used by quorum values may incur poor performance on some database backends which
    # don't have explicit Decimal types due to inefficient floating point conversion. Recommended database backends
    # include MySQL and PostgreSQL.

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'rbitra.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RBITRA_DECISION_PATH = os.path.join(basedir, "decisions")
    RBITRA_PLUGINS_PATH = os.path.join(basedir, "plugins")
