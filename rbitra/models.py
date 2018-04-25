from rbitra import db


class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    any_member_may_create_orgs = db.Column(db.Boolean, default=True)

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fqdn = db.Column(db.String(128))
    port = db.Column(db.Integer, default=443)

    def __repr__(self):
        return 