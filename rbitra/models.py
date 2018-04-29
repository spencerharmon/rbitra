from rbitra import db


class Configuration(db.Model):
    name = db.Column(db.String(64), primary_key=True, unique=True)
    any_member_may_create_orgs = db.Column(db.Boolean, default=True)
    server = db.Column(db.Integer, db.ForeignKey('server.id'))


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fqdn = db.Column(db.String(128))
    port = db.Column(db.Integer, default=443)

    def __repr__(self):
        return '{}:{}'.format(self.fqdn, self.port)


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))


class MemberDigest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.Integer, db.ForeignKey('member.id'))
    digest = db.Column(db.String(160))
