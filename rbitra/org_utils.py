from rbitra import db
from rbitra.models import Organization, Configuration

#localsrv = Configuration.query.filter_by(name='current_config').first().server
#def create_org(name, *, srv=Configuration.query.filter_by(name='current_config').first().server):
def create_org(name, srv):

    #creates an organization.
    #API resource is not exposed to specify server. local server is used by default.

    org = Organization(name=name, server=srv)
    db.session.add(org)
    db.session.commit()
