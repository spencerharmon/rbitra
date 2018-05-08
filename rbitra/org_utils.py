from rbitra import db
from rbitra.models import Organization, Configuration, OrgMember
from rbitra.api_errors import DefaultServerUnconfigured
from uuid import uuid4

def create_org(name, srv=None, uuid=None):
    """
    creates an organization.
    API resource is not exposed to specify server. local server is used by default.
    """
    if uuid is None:
        uuid = str(uuid4())
    if srv is None:
        try:
            qry = Configuration.query.filter_by(name='current_config').first()
            localsrv = qry.server
        except AttributeError as e:
            raise DefaultServerUnconfigured from e
        org = Organization(name=name, server=localsrv, uuid=uuid)
        db.session.add(org)
        db.session.commit()
        return org
    else:
        org = Organization(name=name, server=srv, uuid=uuid)
        db.session.add(org)
        db.session.commit()
        return org


def add_member_to_org(member, org):
    member_org = OrgMember(member=member.uuid, org=org.uuid)
    db.session.add(member_org)
    db.session.commit()
