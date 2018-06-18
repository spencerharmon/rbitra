from rbitra.models import Plugin
from rbitra import db
from dulwich import porcelain
from rbitra.protoplugin import ProtoPlugin
from importlib.machinery import SourceFileLoader
from flask import current_app
import os


def install_plugin(git_url=None):
    repo = clone_plugin_repo(git_url)
    plugin_instance = initialize_plugin_metadata(repo.path)

    db.session.add(plugin_instance)
    db.session.commit()
    return plugin_instance


def clone_plugin_repo(git_url):
    """
    clones git repo containing plugin module to plugins directory.
    :param git_url:
    :return: dulwich repo object
    """
    module_path = "testpath"
    try:
        os.mkdir(current_app.config["RBITRA_PLUGINS_PATH"])
        os.mkdir(os.path.join(current_app.config["RBITRA_PLUGINS_PATH"], module_path))
    except FileExistsError:
        pass

    repo = porcelain.clone(
        git_url,
        target="{}/{}".format(
            current_app.config["RBITRA_PLUGINS_PATH"],
            git_url.replace('/', '-')
        )
    )
    return repo


def initialize_plugin_metadata(path):
    """

    :param path: path to local git repo in valid plugin format
    :return: Plugin (db) object
    """
    module = SourceFileLoader('plugin', os.path.join(path, '__init__.py')).load_module()
    plugin = Plugin(
        title=module.details["title"],
        uuid=module.details["uuid"],
        module_name=module.details["module_name"],
        path=path.replace(current_app.config["RBITRA_PLUGINS_PATH"], '')
    )
    #todo: marshall the data in plugin's __init__.py
    return plugin


def load_plugin_module(plugin):
    module = SourceFileLoader(
        'plugin',
        '{}/{}/{}'.format(
            current_app.config["RBITRA_PLUGINS_PATH"],
            plugin.path,
            '__init__.py'
        )
    ).load_module()
    return module


def load_plugin(decision):
    plugin = Plugin.query.filter_by(
        uuid=decision.plugin
    ).first()
    module = load_plugin_module(plugin)
    return ProtoPlugin(decision, module)


def list_plugin_actions(plugin):
    """
    :return: dict of available actions in plugin
        dict is in format:
        {'action_name': {
            'description': 'description of action'
            'argument_keys_list': ['arg1', 'arg2', et c..]
            'lead_role_req': Bool
        }
    """
    module = load_plugin_module(plugin)

    valid_actions = {}
    for action in module.valid_actions.keys():
        # {'action': ['arg1', 'arg2']}
        valid_actions[action] = {
            'description': module.valid_actions[action]['description'],
            'argument_keys_list': list(module.valid_actions[action]["arg_schema"]().__dict__[declared_fields].keys()),
            'lead_role_req': module.valid_actions[action]['lead_role_req']
        }

    return valid_actions
