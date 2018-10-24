from rbitra import db
from uuid import uuid4
from


class Configuration(db.Model):
    name = db.Column(db.String(64), primary_key=True, unique=True)
    any_member_may_create_orgs = db.Column(db.Boolean, default=True)
    open_enrollment = db.Column(db.Boolean, default=True)
    decision_path = db.Column(db.String(128))
    public_org = db.Column(db.String, db.ForeignKey('organization.uuid'))


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fqdn = db.Column(db.String(128))
    port = db.Column(db.Integer, default=443)

    def __repr__(self):
        return '{}:{}'.format(self.fqdn, self.port)


class Organization(db.Model):
    '''
    Key concepts:
        member_role: This is the role that signifies the membership to this
            organization, therefore, all members of an organization have
            this role.
        mod_role: Members of the organization's mod role have the exclusive
            permission to create decisions flagged with mod_role_req.
            Default plugin meta_plugin has functions create_policy(),
            create_role(), and add_member_to_org(), which are flagged
            with this property.
    '''
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))
    member_role = db.Column(db.String, db.ForeignKey('role.uuid'))
    mod_role = db.Column(db.String, db.ForeignKey('role.uuid'))


class OrganizationLink(db.Model):
    org_a = db.Column(db.String, db.ForeignKey('organization.uuid'), primary_key=True)
    org_b = db.Column(db.String, db.ForeignKey('organization.uuid'), primary_key=True)
    role = db.Column(db.String, db.ForeignKey('role.uuid'))


class Member(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))


class MemberDigest(db.Model):
    member = db.Column(db.String(36), db.ForeignKey('member.uuid'), primary_key=True)
    digest = db.Column(db.String(160))


class Decision(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    title = db.Column(db.String(512))
    org = db.Column(db.String(36), db.ForeignKey('organization.uuid'))
    author = db.Column(db.String(36), db.ForeignKey('member.uuid'))
    plugin = db.Column(db.Integer, db.ForeignKey('plugin.uuid'))
    directory = db.Column(db.String(512))
    policy = db.Column(db.String(36), db.ForeignKey('policy.uuid'))


class Plugin(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(128), unique=True)
    module_name = db.Column(db.String(128))
    path = db.Column(db.String(1024), unique=True)


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
    policy = db.relationship('policy', back_populates='members')
    member = db.relationship



class Policy(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    org = db.Column(db.String(36), db.ForeignKey('organization.uuid'))
    quorum = db.Column(db.Numeric(precision=3, scale=3))
    roles = db.relationship('RolePolicy', back_populates='policy')
    member = db.relationship('PolicyMember', back_populates='policy')


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
