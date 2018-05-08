
from rbitra import db
from rbitra.models import Configuration, Decision, Plugin, Organization, Member
from rbitra.api_errors import FailedToCreateDecision, DataLoadError
from rbitra.pluginproto import PluginProto
from uuid import uuid4
from dulwich import porcelain
import json
import importlib


class DecisionUtils(object):
    def __init__(self, *, uuid=None, title=None, plugin=None, member=None, org=None, directory=None):
        self.decision = Decision()
        self.decision.uuid = uuid
        self.decision.title = title
        self.decision.author = member
        self.decision.org = org
        self.decision.plugin = plugin
        self.decision.directory = directory

        self.author = None
        self.plugin = None
        self.org = None

    def default_decision_title(self):
        return "Default Decision Title"

    def load_models(self):
        if(
                self.author is None |
                self.plugin is None |
                self.org is None
        ):
            items = {
                "author": Member.query.filter_by(uuid=self.decision.author).first(),
                "plugin": Plugin.query.filter_by(uuid=self.decision.plugin).first(),
                "org": Organization.query.filter_by(uuid=self.decision.org).first()
            }
            for typ, value in items:
                if value is None:
                    raise DataLoadError(typ)
            self.author = items["author"]
            self.plugin = items["plugin"]
            self.org = items["org"]

    def ensure_valid_values(self):
        self.load_models()
        if self.decision.title is None:
            self.decision.title = self.default_decision_title()

        if self.decision.directory is None:
            self.decision.directory = self.decision.uuid

    def create_decision(self):
        try:
            assert self.decision.uuid is None
            self.decision.uuid = uuid4()
            self.ensure_valid_values()
            db.session.add(self.decision)
            db.session.commit()

            full_path = self.gen_full_path()
            file_name = "rbitra.json"
            data = self.gen_repo_description_json()
            message = "Repository created by rbitra. Adding decision metadata in rbitra.json."
            self.modify_add_commit_file(full_path, file_name, data, message)

            self.init_plugin()
        except Exception as e:
            raise FailedToCreateDecision(str(e), self.decision.__dict__)


    def modify_add_commit_file(self, repo_path, file_name, new_contents, message):
        """
        takes the name of a file and arbitrary data and commits it to
        :param repo_path: path to git repo
        :param file_name: string; path relative to tld of repo
        :param new_contents: data that will be written to file
        :param message: string; commit message for git
        :return: None
        """
        repo = porcelain.init(repo_path)

        file_path = "{}/{}".format(repo_path, file_name)
        rbitra_datafile = open(file_path)
        rbitra_datafile.write(new_contents)
        rbitra_datafile.close()

        porcelain.add(repo, file_name)
        porcelain.commit(repo, message)

    def gen_full_path(self):
        full_path = "{}/{}/{}".format(
            Configuration.query(name="current_config").first().decision_path,
            self.decision.uuid,
            self.decision.dir
        )
        return full_path

    def init_plugin(self):
        plugin_name = "rbitra.plugins.{}".format(
            Plugin.query.filer_by(
                uuid=self.decision.plugin
            ).first().module_name
        )
        plugin = importlib.import_module(plugin_name)
        plugin.decision = self.decision
        plugin.init_decision_repo()

    def gen_repo_description_json(self):
        self.load_models()

        data = {
            "Decision": self.decision.__dict__,
            "Organization": self.org.__dict__,
            "Member": self.author.__dict__,
            "plugin": self.plugin.__dict__,
        }
        return json.dumps(data)

    # todo: @
    def submit_approval():
        db.Model

