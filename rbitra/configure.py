from rbitra import db
from rbitra.models import Configuration, Server


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
    DEFAULT_CONFIG = Configuration(
        name='current_config',
        any_member_may_create_orgs=True,
        server=srv
    )
    db.session.add(DEFAULT_CONFIG)
    db.session.commit()
