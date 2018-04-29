from rbitra import db
from rbitra.models import Organization, Configuration
from rbitra.api_errors import DefaultServerUnconfigured
from flask_apiexceptions import ApiError, ApiException

#localsrv = Configuration.query.filter_by(name='current_config').first().server
#def create_org(name, *, srv=Configuration.query.filter_by(name='current_config').first().server):
def create_org(name, srv=None):
    """
    creates an organization.
    API resource is not exposed to specify server. local server is used by default.
    """
    if srv is None:
        try:
            qry = Configuration.query.filter_by(name='current_config').first()
            localsrv = qry.server
        except AttributeError:
            raise DefaultServerUnconfigured
        org = Organization(name=name, server=localsrv)
        db.session.add(org)
        db.session.commit()
    else:
        org = Organization(name=name, server=srv)
        db.session.add(org)
        db.session.commit()

