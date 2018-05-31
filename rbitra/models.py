from rbitra import db


class Configuration(db.Model):
    name = db.Column(db.String(64), primary_key=True, unique=True)
    any_member_may_create_orgs = db.Column(db.Boolean, default=True)
    decision_path = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fqdn = db.Column(db.String(128))
    port = db.Column(db.Integer, default=443)

    def __repr__(self):
        return '{}:{}'.format(self.fqdn, self.port)


class Organization(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))


class Member(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))


class MemberDigest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.String(36), db.ForeignKey('member.uuid'))
    digest = db.Column(db.String(160))


class OrgMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.String(36), db.ForeignKey('member.uuid'))
    org = db.Column(db.String(36), db.ForeignKey('organization.uuid'))


class Decision(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    title = db.Column(db.String(512))
    org = db.Column(db.String(36), db.ForeignKey('organization.uuid'))
    author = db.Column(db.String(36), db.ForeignKey('member.uuid'))
    plugin = db.Column(db.Integer, db.ForeignKey('plugin.uuid'))
    directory = db.Column(db.String(512))


class Plugin(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(128), unique=True)
    module_name = db.Column(db.String(128))
    path = db.Column(db.String(1024), unique=True)
