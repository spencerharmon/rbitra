from rbitra.decision_utils import gen_full_path
from rbitra.api_errors import RepoCouldNotBeLoaded, PluginMethodUndefined
from dulwich import porcelain


class PluginProto(object):
    """
    PluginProto defines the methods rbitra uses that generalize the operations for all plugins.

    Plugins must support loading arbitrary models by name stored in a database.
    The contents of a plugin are represented as unstructured data. Because one of the stated
    goals of rbitra is to support decision-making for Git repositories, the unstructured data
    is represented by the contents of a Git repository. Plugins can leverage the repository and
    represent their decision's data any way they see fit.
    Future support for nosql databases for representing decision data is possible, but since
    version control is a stated goal and no modules are currently extant to bridge the gap
    between git and unstructured document databases, Git is the first choice in spite of
    the slower transaction rate.
    """
    def __init__(self, decision):
        """

        :param decision: Decision (db) object
        """
        self.decision = decision
        self.type = None
        self.valid_actions = None
        self.load_repo()

    def load_repo(self):
        try:
            self.repo = porcelain.init(gen_full_path(self.decision))
        except:
            raise
#            raise RepoCouldNotBeLoaded(self.decision)

    def parse_repo(self):
        '''
        parse_repo should ensure that the data in the repo is compatible with the plugin, return
        a JSON object containing all relevant information about the decision represented by the
        repo, and raise an exception otherwise.
        :returns: JSON
        '''
        raise PluginMethodUndefined("parse_repo()")

    def file_list(self):
        """
        :return: list of files in repo
        """
        return list(self.repo.open_index())

    def check_and_load_vars(self, file):
        """
        Converts contents of JSON file to relevant class members, otherwise raises an exception
        :param file:
        :return:
        """
        raise PluginMethodUndefined("check_and_load_vars()")

    def init_decision_repo(self):
        """
        Does any work necessary at the time a decision's repo is created.

        :return:
        """
        raise PluginMethodUndefined("init_decision_repo()")

    def list_actions(self):
        """

        :return: dict of available actions in plugin
        """

        return self.valid_actions

    def enact(self):
        """
        enact is the primary function of a plugin. It's what it "does."
        :return:
        """

        raise PluginMethodUndefined("enact()")