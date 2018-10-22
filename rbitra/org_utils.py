from rbitra import db
from rbitra.models import Organization, Configuration, Member, MemberRole, OrganizationLink
from rbitra.role_utils import add_member_to_role, create_role
from rbitra.api_errors import ServerUnconfigured
from rbitra.policy_utils import create_policy
from rbitra.models import Configuration
from uuid import uuid4
import json


def create_org(name, initial_members=[], is_public=False):
    """
    Creates and sets default member_role and sets this as mod_role.
    Adds initial member(s) to member_role
    Creates OrganizationLink to the members of the public organization's member_role.
    is_public disables the linking behavior. This is used only when creating the public organization during
    installation.
    """
    print(initial_members)
    with db.session.no_autoflush:
        org_uuid = uuid4().__str__()
        role = create_role('Member of {}'.format(name), org_uuid)
        org = Organization(name=name, uuid=org_uuid, member_role=role.uuid, mod_role=role.uuid)
        for member in initial_members:
            if member is not None:
                member_role = MemberRole(member=member, role=role.uuid)
                db.session.add(member_role)
        if is_public:
            org_opt_dict = {role.uuid: {}}
            import pprint
            pprint.pprint(org_opt_dict)
            create_policy('Public Members', org_uuid, org_opt_dict)
        else:
            config = Configuration.query.filter_by(name='current_config').first()
            pub_org = Organization.query.filter_by(uuid=config.public_org).first()

            org_opt_dict = {role.uuid: {}}
            create_policy('Organization Members', org_uuid, org_opt_dict)

            pub_opt_dict = {role.uuid: {}, pub_org.member_role: {}}
            create_policy('Public', org_uuid, pub_opt_dict)

            orglink = OrganizationLink(org_a=org.uuid, org_b=pub_org.uuid, role=pub_org.member_role)
            db.session.add(orglink)
        db.session.add(org)
        db.session.commit()
        return org


def add_member_to_org(member, org):
    member_role = MemberRole(member=member.uuid, role=org.member_role)
    db.session.add(member_role)
    db.session.commit()


def add_member_to_org_by_uuid(member_uuid, org_uuid):
    member = Member.query.filter_by(uuid=member_uuid).first()
    org = Organization.query.filter_by(uuid=org_uuid).first()
    add_member_to_org(member, org)