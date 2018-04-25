from rbitra import db
from rbitra.models import Configuration

DEFAULT_CONFIG = Configuration(
    name='current_config',
    any_member_may_create_orgs=True
)


def set_any_member_may_create_orgs(b):
    current_config = Configuration.query.filter_by(config_name='current_config').first()
    current_config['any_member_may_create_orgs'] = b
    db.session.commit()


def set_default_config():
    db.session.add(DEFAULT_CONFIG)
    db.session.commit()
