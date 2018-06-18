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
    lead_role = db.Column(db.Integer, db.ForeignKey('role.uuid'))

class Member(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))


class MemberDigest(db.Model):
    member = db.Column(db.String(36), db.ForeignKey('member.uuid'), primary_key=True)
    digest = db.Column(db.String(160))


class OrgMember(db.Model):
    member = db.Column(db.String(36), db.ForeignKey('member.uuid'), primary_key=True)
    org = db.Column(db.String(36), db.ForeignKey('organization.uuid'), primary_key=True)


class Decision(db.Model):
    uuid = db.Column(db.String(36), unique=True, primary_key=True)
    title = db.Column(db.String(512))
    org = db.Column(db.String(36), db.ForeignKey('organization.uuid'))
    author = db.Column(db.String(36), db.ForeignKey('member.uuid'))
    plugin = db.Column(db.Integer, db.ForeignKey('plugin.uuid'))
    directory = db.Column(db.String(512))
    policy = db.Column(db.String(36), db.ForeignKey('policy.uuid'))
    organization_read = db.Column(db.Boolean())
    organization_write = db.Column(db.Boolean())
    public_read = db.Column(db.Boolean())
    public_write = db.Column(db.Boolean())


class Plugin(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(128), unique=True)
    module_name = db.Column(db.String(128))
    path = db.Column(db.String(1024), unique=True)


class Approval(db.Model):
    member = db.Column(db.String(36), db.ForeignKey('member.uuid'), primary_key=True)
    decision = db.Column(db.String(36), db.ForeignKey('decision.uuid'), primary_key=True)


class Role(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    org_decisions_allowed = db.Column(db.Boolean())
    pub_decisions_allowed = db.Column(db.Boolean())


class MemberRole(db.Model):
    member = db.Column(db.String(36), db.ForeignKey('member.uuid'), primary_key=True)
    role = db.Column(db.String(36), db.ForeignKey('role.uuid'), primary_key=True)


class Policy(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))


class PolicyRole(db.Model):
    """
    defines RO/RW permissions on a decision for roles associated with a policy.
    Additionally, members with roles that have write permissions for decisions
    associated with this policy may create decisions that use this policy.
    """
    policy = db.Column(db.String(36), db.ForeignKey('policy.uuid'), primary_key=True)
    role = db.Column(db.String(36), db.ForeignKey('role.uuid'), primary_key=True)
    read = db.Column(db.Boolean())
    write = db.Column(db.Boolean())


