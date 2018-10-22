from rbitra import db


class Role(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    org = db.Column(db.String(36), db.ForeignKey('organization.uuid'))