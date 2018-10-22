from rbitra import db


class Plugin(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(128), unique=True)
    module_name = db.Column(db.String(128))
    path = db.Column(db.String(1024), unique=True)
