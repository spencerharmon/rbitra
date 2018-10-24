from rbitra import db


class Decision(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    title = db.Column(db.String(512))
    org = db.relationship('Organization')
    author = db.relationship('Member')
    plugin = db.relationship('Plugin')
    directory = db.Column(db.String(512))
    policy = db.relationship('Policy')
    approvals = db.relationship('Approval', back_populates='decision')
