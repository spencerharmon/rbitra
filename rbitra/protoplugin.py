from rbitra import decision_utils
from rbitra.api_errors import RepoCouldNotBeLoaded, PluginMethodUndefined, PluginContentsError
from dulwich.repo import Repo
import json


class ProtoPlugin(object):
    """
    ProtoPlugin defines the methods rbitra uses that generalize the operations for all plugins.

    """
    def __init__(self, decision, plugin_module):
        """

        :param decision: Decision (db) object
        """
        self.decision = decision
        self.plugin_module = plugin_module
        self.type = None
        self.attachments = []
        self.actions = {}
        self.repo = Repo.discover(start=decision_utils.gen_full_path(self.decision))

    def file_list(self):
        """
        :return: list of files in repo
        """
        return list(self.repo.open_index())

    def parse_repo(self):
        '''
        parse_repo ensures that the data in the repo is compatible with the plugin, returns
        a JSON object containing all relevant information about the decision represented by the
        repo, and raises an exception otherwise.
        :returns: JSON
        '''
        for file in self.file_list():
            if file.name is "rbitra_info.json":
                self.check_and_load_actions(file)
            else:
                self.attachments.append(file)

    def init_decision_repo(self):
        """
        If defined in module, does any work necessary at the
        time a decision's repo is created.
        :return: None
        """
        if "init_decision_repo" in self.plugin_module.valid_actions:
            self.plugin_module.valid_actions["init_decision_repo"]()

    def list_actions(self):
        """
        :return: dict of available actions in plugin
        """
        return self.plugin_module.valid_actions

    def check_and_load_actions(self, file):
        """
        Converts contents of JSON file representing actions to relevant class member,
        otherwise raises an exception.
        :param file:
        :return:
        """
        contents = json.load(file)
        try:
            method_list = []
            for k, v in self.plugin_module.valid_actions:
                method_list.append(k)
            if contents["action"] not in method_list:
                raise PluginContentsError
            for action in contents["actions"]:
                self.check_action_arguments(action)
            self.actions = contents["actions"]
        except AttributeError or marshmallow.ValidationError:
            raise PluginContentsError(file.name, self.__name__)

    def check_action_arguments(self, action):
        """
        initializes marshmallow schema for action with provided argument dict
        :param action: single-member dict whose key represents the method to be executed
        :return: None. Raises marshmallow ValidationError if
        """
        #TODO: catch invalid action strings
        schema = self.plugin_module.valid_actions[action.keys()[1]]["arg_schema"]()
        schema.load(action.values()[1])

    def enact(self):
        """
        enact is the primary function of a plugin. It's what it "does."
        :return:
        """
        #TODO: catch invalid action strings
        for action, arguments in self.actions:
            self.plugin_module.valid_actions[action]["action"](arguments, attachments=self.attachments)
