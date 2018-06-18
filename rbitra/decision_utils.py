
from rbitra import db
from rbitra.models import Configuration, Decision, Plugin, Organization, Member, Approval, MemberRole
from rbitra.api_errors import FailedToCreateDecision, DataLoadError, PermissionsError
from rbitra.plugin_utils import load_plugin, list_plugin_actions
from rbitra.schema import DecisionSchema, OrganizationSchema, MemberSchema, PluginSchema
from uuid import uuid4
from dulwich import porcelain
import json
import os
import re
import pprint


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


    def create_decision_repo(self, path):
        os.makedirs(path)
        repo = porcelain.init(path)
        self.repo = repo

    def file_list(self):
        """
        :return: list of files in repo
        """
        full_path = gen_full_path(self.decision)

        file_list = ['{}/{}'.format(full_path, f)
                     for f in os.listdir(full_path)
                     if os.path.isfile('{}/{}'.format(full_path, f))]
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
            "Decision": ds.dump(self.decision)[0],
            "Organization": orgsch.dump(self.org)[0],
            "Member": ms.dump(self.author)[0],
            "Plugin": ps.dump(self.plugin)[0]
        }
        return json.dumps(data, indent=2)

    def set_actions(self, actions):
        for action, args in actions.items():
            for attrib in list_plugin_actions(self.plugin)[action]:
                if attrib['lead_role_req']:
                    org = Organization.query.filter_by(uuid=self.decision.org).first()
                    member_list = [memberrole.member
                                   for memberrole in MemberRole.query.filter_by(uuid=org.lead_role)]
                    if self.decision.author not in member_list:
                        raise PermissionsError(
                            'Member {} cannot create decision with action {}.'.format(
                                self.decision.author,
                                action
                            )
                        )
                    else:
                        self.append_action({action: args})
                else:
                    self.append_action({action: args})

    def append_action(self, action):
        plugin = load_plugin(self.decision)
        plugin.check_action_arguments(action)
        contents = {}
        for file in self.file_list():
            if re.match(".*rbitra\.json$", file):
                with open(file) as f:
                    contents.update(json.load(f))
                contents["actions"] = action
                self.modify_add_commit_file(
                    self.decision.directory,
                    file,
                    json.dumps(contents, indent=2),
                    "Rbitra appended action: {}".format(json.dumps(action))
                )
    # todo: @
    def approved_by(self, member_uuid):
        approval = Approval()
        approval.member = member_uuid
        approval.decision = self.decision.uuid
        self.check_quorum()

    def check_quorum(self):
        '''
        Determines whether a decision's quorum has been met.
        :return: bool, True if quorum is met, False otherwise.
        '''
        quorum_threshold = self.determine_quorum()
        weighted_total = 0
        weighted_approval = 0
        for member_uuid in self.decision_makers():
            weighted_total += 1 #TODO: add weights here instead of 1
            if member_uuid in self.approval_list():
                weighted_approval += 1 #TODO: add weights here instead of 1
        if quorum_threshold < weighted_approval / weighted_total:
            return True
        else:
            return False

    def approval_list(self):
        '''

        :return: list of member UUIDs that approve of self.decision
        '''
        return [record.member
                for record in Approval.query.filter_by(decision=self.decision.uuid)]

    def decision_makers(self):
        '''

        :return:list of members' uuids with roles given RW access by the decision's policy
        '''
        return [memberrole.member
                for policy in Policy.query.filter_by(uuid=self.decision.policy)
                for policyrole in PolicyRole.query.filter_by(policy=policy.uuid)
                for memberrole in MemberRoles.query.filter_by(role=policyrole.role)]