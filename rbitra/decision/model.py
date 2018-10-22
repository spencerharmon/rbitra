from rbitra import db


class Decision(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    title = db.Column(db.String(512))
    org = db.Column(db.String(36), db.ForeignKey('organization.uuid'))
    author = db.Column(db.String(36), db.ForeignKey('member.uuid'))
    plugin = db.Column(db.Integer, db.ForeignKey('plugin.uuid'))
    directory = db.Column(db.String(512))
    policy = db.Column(db.String(36), db.ForeignKey('policy.uuid'))
