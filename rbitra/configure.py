from rbitra import db
from rbitra.models import Configuration, Server
from rbitra.member_utils import create_member
from rbitra.org_utils import create_org, add_member_to_org
from flask import current_app

def set_any_member_may_create_orgs(b=True):
    current_config = Configuration.query.filter_by(config_name='current_config').first()
    current_config['any_member_may_create_orgs'] = b
    db.session.commit()


def create_local_server():
    server = Server(
        id=1,
        fqdn='localhost',
        port=443
    )
    db.session.add(server)
    db.session.commit()


def set_default_config():
    create_local_server()
    srv = Server.query.get(1).id
    default_config = Configuration(
        name='current_config',
        any_member_may_create_orgs=True,
        server=srv,
        decision_path=current_app.config['RBITRA_DECISION_PATH']
    )
    db.session.add(default_config)
    member = create_member("default", "default")
    org = create_org("default")
    add_member_to_org(member, org)
    db.session.commit()
