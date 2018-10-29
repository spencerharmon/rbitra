from rbitra import db


class Policy(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    org = db.relationship('Organization')
    quorum = db.Column(db.Numeric(precision=3, scale=3))
    roles = db.relationship('RolePolicy', back_populates='policy')
    members = db.relationship('PolicyMember', back_populates='policy')