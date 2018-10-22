from rbitra import db


class Organization(db.Model):
    """
    Key concepts:
        member_role: This is the role that signifies the membership to this
            organization, therefore, all members of an organization have
            this role.
        mod_role: Members of the organization's mod role have the exclusive
            permission to create decisions flagged with mod_role_req.
            Default plugin meta_plugin has functions create_policy(),
            create_role(), and add_member_to_org(), which are flagged
            with this property.
    """
    uuid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    server = db.Column(db.Integer, db.ForeignKey('server.id'))
    member_role = db.Column(db.String, db.ForeignKey('role.uuid'))
    mod_role = db.Column(db.String, db.ForeignKey('role.uuid'))
