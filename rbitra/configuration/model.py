from rbitra import db


class Configuration(db.Model):
    name = db.Column(db.String(64), primary_key=True, unique=True)
    any_member_may_create_orgs = db.Column(db.Boolean, default=True)
    open_enrollment = db.Column(db.Boolean, default=True)
    decision_path = db.Column(db.String(128))
    public_org = db.Column(db.String, db.ForeignKey('organization.uuid'))
