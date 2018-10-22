from rbitra import decision_utils
from rbitra.api_errors import RepoCouldNotBeLoaded, PluginMethodUndefined, PluginContentsError
from dulwich.repo import Repo
import marshmallow
import json
import re

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
        self.du = decision_utils.DecisionUtils(decision)

        self.parse_repo()

    def parse_repo(self):
        '''
        parse_repo ensures that the data in the repo is compatible with the plugin, returns
        a JSON object containing all relevant information about the decision represented by the
        repo, and raises an exception otherwise.
        :returns: JSON
        '''
        for filename in self.du.file_list():
            if re.match(".*/rbitra.json$", filename):
                with open(filename) as file:
                    self.check_and_load_actions(file)
            else:
                self.attachments.append(filename)

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
            for k, v in self.plugin_module.valid_actions.items():
                method_list.append(k)
            if "Actions" in contents:
                for action, arguments in contents["Actions"].items():
                    if action not in method_list:
                        raise PluginContentsError
                    self.check_action_arguments(actions={action: arguments})
                    self.actions = contents["Actions"]
        except (AttributeError, marshmallow.ValidationError):
            raise PluginContentsError(file.name, self.__name__)

    def check_action_arguments(self, actions=None):
        """
        initializes marshmallow schema for action with provided argument dict
        :param actions: actions dict
        :return: None. Raises marshmallow ValidationError if
        """
        #TODO: catch invalid action strings
        if actions is not None:
            dict = actions
        else:
            dict = self.actions
        for action, arguments in dict.items():
            try:
                    schema = self.plugin_module.valid_actions[action]["arg_schema"]()
                    schema.dump(arguments)
            except AttributeError:
                raise PluginMethodUndefined(action)

    def enact(self):
        """
        enact executes the actions specified from the plugin specified in the decision.
        :return:
        """
        #TODO: catch invalid action strings
        for action, arguments in self.actions.items():
            self.plugin_module.valid_actions[action]["action"](arguments, attachments=self.attachments)
