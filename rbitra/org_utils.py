import rbitra
from models import Organization, Configuration

def create_local_org(name, *, localserver=Configuration.query.filter_by(name='current_config')  ):
    org = Organization(name=name, server=localserver)
    rbitra.db.session.add(org)

def add_remote_org(name, server):
    pass