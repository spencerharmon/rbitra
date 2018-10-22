from rbitra import db


class Member(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))

