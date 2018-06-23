from rbitra import db
from rbitra.models import Configuration, Server
from rbitra.member_utils import create_member
from rbitra.org_utils import create_org, add_member_to_org
from flask import current_app

def get_public_config_opts():
    org = create_org("Public", is_public=True)
    ret = {
        'name': 'current_config',
        'any_member_may_create_orgs': True,
        'open_enrollment': True,
        'decision_path': current_app.config['RBITRA_DECISION_PATH'],
        'public_org': org.uuid
    }
    return ret


def get_private_config_opts():
    '''
    create default member and add to public org since open_enrollment is off
    :return: dict of configuration options
    '''
    member = create_member("default", "default", "default@localhost")
    org = create_org("Public", initial_members=[member.uuid], is_public=True)
    ret = {
        'name': 'current_config',
        'any_member_may_create_orgs': False,
        'open_enrollment': False,
        'decision_path': current_app.config['RBITRA_DECISION_PATH'],
        'public_org': org.uuid
    }
    return ret


def set_config(preset='public', **kwargs):
    config_opts = None
    if preset == 'public':
        config_opts = get_public_config_opts()
    elif preset == 'private':
        config_opts == get_private_config_opts()
    else:
        # convert kwargs to dict for compatibility with preset option functions
        # todo: support update operations (load config into dict with marshmallow and update records with kwargs)
        config_opts = {k: v for k, v in kwargs}
    db.session.add(Configuration(**config_opts))
    db.session.commit()
