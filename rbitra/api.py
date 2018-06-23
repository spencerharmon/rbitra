from rbitra import create_app
from flask_restful import Api, Resource, reqparse
from rbitra.configure import set_config
from rbitra.org_utils import create_org
from rbitra.member_utils import create_member
from rbitra.decision_utils import DecisionUtils
from rbitra.plugin_utils import install_plugin, get_plugin_actions
from rbitra.models import Decision, Plugin, Member
from rbitra.schema import OrganizationSchema, MemberSchema, DecisionSchema, PluginSchema
import json
from rbitra.auth import auth

api = Api(create_app())


class Install(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'preset',
            type=str,
            help='Set wither public or private preset. Default: public'
        )

    def get(self):
        args = self.parser.parse_args()
        if args['preset'] is not None:
            set_config(preset=args['preset'])
        else:
            set_config()


api.add_resource(Install, '/install')


class CreateOrg(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('org_name', type=str, help='Name of an organization.')
        self.parser.add_argument(
            'initial_members',
            type=list,
            help='List of members (in addition to the authenticated member) to add to the organization upon creation.'
        )


    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        schema = OrganizationSchema()

        member = Member.query.filter_by(email=auth.username()).first()
        initial_members = [member.uuid]
        if args['initial_members'] is not None:
            initial_members.append(args['initial_members'])
        org = create_org(args['org_name'], initial_members)
        return schema.dumps(org)


api.add_resource(CreateOrg, '/create/org')


class CreateMember(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'member_name',
            type=str,
            help='Username of new member.',
            required=True
        )
        self.parser.add_argument(
            'password',
            type=str,
            help='Password for new account.',
            required=True
        )
        self.parser.add_argument(
            'email',
            type=str,
            help='Member\'s email address.',
            required=True
        )

    def post(self):
        args = self.parser.parse_args()
        schema = MemberSchema()
        member = create_member(args['member_name'], args['password'], args['email'])
        return schema.dumps(member)


api.add_resource(CreateMember, '/create/member')


class CreateDecision(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'title',
            type=str,
            help='A title for the decision.',
            required=True
        )
        self.parser.add_argument(
            'plugin',
            type=str,
            help='UUID of plugin used by the decision',
            required=True
        )
        self.parser.add_argument(
            'org',
            type=str,
            help='UUID of organization.',
            required=True
        )
        self.parser.add_argument(
            'directory',
            type=str,
            help='Name of the decision repository\'s directory',
            required=True
        )
        self.parser.add_argument(
            'actions',
            type=str,
            help='JSON actions dictionary for ProtoPlugin.' +
                 'Valid format is provided at the "/plugin/[plugin name/uuid]/valid_actions" resource ' +
                 'or the /decision/[decision uuid]/valid_actions resource.',
            required=True
        )

    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        member = Member.query.filter_by(email=auth.username()).first()
        decision = Decision(
            title=args["title"],
            plugin=args["plugin"],
            author=member.uuid,
            org=args["org"],
            directory=args["directory"]
        )
        actions = json.loads(args["actions"])
        du = DecisionUtils(decision, actions=actions)
        schema = DecisionSchema()
        decision = du.create_decision()
        return schema.dumps(decision)


api.add_resource(CreateDecision, '/create/decision')


class PluginValidActions(Resource):

    def get(self, title):
        plugin = Plugin.query.filter_by(title=title).first()
        return json.dumps(get_plugin_actions(plugin))


api.add_resource(PluginValidActions, '/plugin/<string:title>/valid_actions')

class InstallPlugin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'git_url',
            type=str,
            help='URL for repository containing plugin.',
            required=True
        )

    def post(self):
        args = self.parser.parse_args()
        schema = PluginSchema()
        member = install_plugin(args['git_url'])
        return schema.dumps(member)


api.add_resource(InstallPlugin, '/install/plugin')