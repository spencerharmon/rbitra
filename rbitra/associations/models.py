from rbitra import db


class OrganizationLink(db.Model):
    org_a = db.Column(db.String, db.ForeignKey('organization.uuid'), primary_key=True)
    org_b = db.Column(db.String, db.ForeignKey('organization.uuid'), primary_key=True)
    role = db.Column(db.String, db.ForeignKey('role.uuid'))


class Approval(db.Model):
    member_id = db.Column(db.String(36), db.ForeignKey('member.uuid'), primary_key=True)
    decision_id = db.Column(db.String(36), db.ForeignKey('decision.uuid'), primary_key=True)
    member = db.relationship('Member', back_populates='approvals')
    decision = db.relationship('Decision', back_populates='approvals')


class MemberRole(db.Model):
    member_id = db.Column(db.String(36), db.ForeignKey('member.uuid'), primary_key=True)
    role_id = db.Column(db.String(36), db.ForeignKey('role.uuid'), primary_key=True)
    member = db.relationship('Member', back_populates='roles')
    role = db.relationship('Role', back_populates='members')


class PolicyMember(db.model):
    # todo: event listener to update this association
    member_id = db.Column(db.String(36), db.ForeignKey('memberrole.uuid'), primary_key=True)
    policy_id = db.Column(db.String(36), db.ForeignKey('policy.uuid'), primary_key=True)
    policy = db.relationship('Policy', back_populates='members')
    member = db.relationship('Member', back_populates='policies')


class RolePolicy(db.Model):
    """
    Defines observe/participate permissions for a decision with roles associated with this policy. Additionally, members
    with roles that have participate permissions for decisions associated with this policy may create decisions that use
    this policy.
    """
    policy_id = db.Column(db.String(36), db.ForeignKey('policy.uuid'), primary_key=True)
    role_id = db.Column(db.String(36), db.ForeignKey('role.uuid'), primary_key=True)
    policy = db.relationship('Policy', back_populates='roles')
    role = db.relationship('Role', back_populates='policies')

    # observe = read permission
    observe = db.Column(db.Boolean(), default=True)
    # participate = read/write permission
    participate = db.Column(db.Boolean(), default=True)
    quorum_weight = db.Column(db.Integer(), default=1)
