from rbitra import db


class Member(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))
    roles = db.relationship('MemberRoles', back_populates='member')
    approvals = db.relationship('Approvals', back_populates='member')
    policies = db.relationship('PolicyMember', back_populates='member')
    #todo: add support for the relationships below
    #concerns = db.relationship('Concern', back_populates='member')
    #comments = db.relationship('Comment', back_populates='member')
