from rbitra import db


class Decision(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    title = db.Column(db.String(512))
    directory = db.Column(db.String(512))
    org_id = db.Column(db.String(36), db.ForeignKey('organization.uuid'))
    org = db.relationship('Organization')
    author_id = db.Column(db.String(36), db.ForeignKey('member.uuid'))
    author = db.relationship('Member')
    plugin_id = db.Column(db.String(36), db.ForeignKey('plugin.uuid'))
    plugin = db.relationship('Plugin')
    policy_id = db.Column(db.String(36), db.ForeignKey('policy.uuid'))
    policy = db.relationship('Policy')
    approvals = db.relationship('Approval', back_populates='decision')
