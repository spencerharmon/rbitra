from rbitra import db
from rbitra.models import Role, MemberRole
from uuid import uuid4


def create_role(name, org_uuid):
    uuid = str(uuid4())
    role = Role(uuid=uuid, name=name, org=org_uuid)
    db.session.add(role)
    db.session.commit()
    return role


def add_member_to_role(member, role):
    memberrole = MemberRole(member=member.uuid, role=role.uuid)
    db.session.add(memberrole)
    db.session.commit()
