
from rbitra import db
from rbitra.models import Configuration, Decision, Plugin, Organization, Member
from rbitra.api_errors import FailedToCreateDecision, DataLoadError
from rbitra.plugin_utils import load_plugin
from rbitra.schema import DecisionSchema, OrganizationSchema, MemberSchema, PluginSchema
from uuid import uuid4
from dulwich import porcelain
import json
import os
import importlib


def gen_full_path(decision):
    full_path = os.path.join(
        Configuration.query.filter_by(name="current_config").first().decision_path,
        decision.uuid,
        decision.directory
    )
    return full_path


class DecisionUtils(object):
    def __init__(self, decision=None, actions=None):
        self.decision = decision
        self.actions = actions

        self.author = None
        self.plugin = None
        self.org = None
        self.repo = None

    def default_decision_title(self):
        return "Default Decision Title"

    def load_models(self):
        if(
                self.author is None or
                self.plugin is None or
                self.org is None
        ):
            items = {
                "author": Member.query.filter_by(uuid=self.decision.author).first(),
                "plugin": Plugin.query.filter_by(uuid=self.decision.plugin).first(),
                "org": Organization.query.filter_by(uuid=self.decision.org).first()
            }
            for typ, value in items.items():
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
            self.decision.uuid = str(uuid4())
            self.ensure_valid_values()
            db.session.add(self.decision)

            full_path = gen_full_path(self.decision)
            self.create_decision_repo(full_path)


            file_name = "rbitra.json"
            data = self.gen_repo_description_json()
            message = "Repo created by Rbitra. Adding decision metadata in rbitra.json."
            self.modify_add_commit_file(full_path, file_name, data, message)

            if self.actions is not None:
                self.set_actions(self.actions)

            self.init_plugin()

            db.session.commit()
            return self.decision
        except AttributeError as e:
            raise
#            raise FailedToCreateDecision(e)


    def create_decision_repo(self, path):
        os.makedirs(path)
        repo = porcelain.init(path)
        self.repo = repo

    def file_list(self):
        """
        :return: list of files in repo
        """
        full_path = gen_full_path(self.decision)

        file_list = [open('{}/{}'.format(full_path, f), 'w') for r, d, f in os.walk(full_path)]
        return file_list

    def modify_add_commit_file(self, repo_path, file_name, new_contents, message):
        """
        takes the name of a file and arbitrary data and commits it to
        :param repo_path: path to git repo
        :param file_name: string; path relative to tld of repo
        :param new_contents: data that will be written to file
        :param message: string; commit message for git
        :return: None
        """

        file_path = os.path.join(repo_path, file_name)
        with open(file_path, 'w') as rbitra_datafile:
            rbitra_datafile.write(new_contents)
        porcelain.add(self.repo, file_path)
        porcelain.commit(self.repo, message)

    def init_plugin(self):
        plugin = load_plugin(self.decision)
        plugin.init_decision_repo()

    def gen_repo_description_json(self):
        self.load_models()

        ds = DecisionSchema()
        orgsch = OrganizationSchema()
        ms = MemberSchema()
        ps = PluginSchema()
        data = {
            "Decision": ds.dump(self.decision),
            "Organization": orgsch.dump(self.org),
            "Member": ms.dump(self.author),
            "plugin": ps.dump(self.plugin)
        }
        return json.dumps(data)

    def set_actions(self, actions):
        for k,v in actions.items():
            self.append_action({k: v})

    def append_action(self, action):
        plugin = load_plugin(self.decision)
        plugin.check_action_arguments(action)
        contents = {}
        for file in self.file_list():
            if file.name is "rbitra.json":
                contents = json.load(file)
                contents["actions"] = action
                self.modify_add_commit_file(
                    self.decision.directory,
                    file.name,
                    json.dumps(contents),
                    "Rbitra appended action: {}".format(json.dumps(action))
                )
                file.close()
            else:
                file.close()
    # todo: @
    def submit_approval():
        db.Model

