from rbitra import db, exception_handler
from rbitra.models import Organization, Configuration
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
            qry = Configuration.query.filter_by(name='current_config').first().server
        except AttributeError:
            err = ApiError(
                code="Default unavailable.",
                message="Default server not found. Likely need to run /install."
            )
            raise ApiException(status_code=500, error=err)
    else:
        localsrv = srv
    org = Organization(name=name, server=localsrv)
    db.session.add(org)
    db.session.commit()
