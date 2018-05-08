from rbitra import db
from rbitra.pluginproto import PluginProto
from rbitra.api_errors import PluginContentsError
from rbitra.models import Member, Organization, OrgMember
import json


class MetaPlugin(PluginProto):
    """
    The meta plugin is a special plugin that allows the use of decisions to modify rbitra_server's
    configuration, organizational parameters, roles, policies, and membership. This requires special
    permission structure, and access to modify rbitra's database tables for the above.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.valid_actions = {
            "add_member_to_org": {
                "description": "Add Member to Organization",
                "arg_validator": self.check_add_member_to_org_arguments,
                "action": self.add_member_to_org
            }
        }

        self.actions = {}
        self.example_action = {
            "add_member_to_org": {
                "member": self.decision.author,
                "org": self.decision.org
            }
        }
        self.attachments = []

    def parse_repo(self):
        for file in self.file_list():
            if file.name is "metaplugin.json":
                self.check_and_load_vars(file)
            else:
                self.attachments.append(file)

    def check_and_load_vars(self, file):
        if file.name is "metaplugin.json":
            contents = json.load(file)
            try:
                method_list = []
                for k, v in valid_actions:
                    method_list.append(k)
                if contents["action"] not in method_list:
                    raise PluginContentsError
                self.action = contents["action"]
                self.arguments = contents["arguments"]
                self.valid_actions[self.action]["arg_validator"]()
            except AttributeError or PluginContentsError:
                raise PluginContentsError(file.name, self.__name__)
        else:
            return

    def check_action_arguments(self):
        #TODO: catch invalid action strings
        for action, arguments in self.actions:
            if self.valid_actions[action]["arg_validator"](arguments):
                return
            else:
                raise PluginContentsError()

    def check_add_member_to_org_arguments(self, arguments):
        #todo: catch sqlalchemy query errors
        assert "member" in arg.keys()
        assert "org" in arg.keys()
        member = Member.query(uuid=arguments["member"]).first()
        org = Organization.query(uuid=arguments["org"]).first()
        if member is not None and org is not None:
            return True
        else:
            return False

    def add_member_to_org(self, arguments):
        member = Member.query(uuid=arguments["member"]).first()
        org = Organization.query(uuid=arguments.["org"]).first()
        assoc = OrgMember(org, member)
        db.session.add(assoc)
        db.session.commit()

    def argument_check(self):
        for k, v in self.arguments:
            arg_type = self.valid_actions[self.action]["argtypes"][k]
            if v is not arg_type:
                raise PluginContentsError

    def enact(self):
        #TODO: catch invalid action strings
        for action, arguments in self.actions:
            if self.valid_actions[action]["action"](arguments):
                return
            else:
                raise PluginContentsError()


    def init_decision_repo(self):
        pass