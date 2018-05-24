from rbitra.models import Plugin
from rbitra import db
from dulwich import porcelain
import importlib
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
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n{}\n!!!!!!!!!!!!!!!!!!!!!!!!!".format(repo.path))
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
        class_name=module.details["class_name"],
        path=path.replace(current_app.config["RBITRA_PLUGINS_PATH"], '')
    )
    #todo: marshall the data in plugin's __init__.py
    return plugin

def load_plugin(plugin, decision):
    full_path = '{}/{}/{}'.format(
        current_app.config['RBITRA_PLUGINS_PATH'],
        plugin.path,
        '{}{}'.format(
            plugin.module_name,
            '.py'
        )
    )
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!11\nplugins path: {}\n'.format(current_app.config['RBITRA_PLUGINS_PATH']))
    print('!!!!!!!!!!!!!!!!!!!!!!!\nload_plugin full_path: {}\n!!!!!!!!!!!!!!!!'.format(full_path))
    module = SourceFileLoader(plugin.module_name, full_path).load_module()
    plugin_class = getattr(module, plugin.class_name)
    return plugin_class(decision)
