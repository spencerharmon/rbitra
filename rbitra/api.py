from rbitra import create_app
from flask_restful import Api, Resource, reqparse
from rbitra.configure import set_default_config
from rbitra.org_utils import create_org
from rbitra.member_utils import create_member
from rbitra.decision_utils import DecisionUtils
from rbitra.plugin_utils import install_plugin
from rbitra.schema import OrganizationSchema, MemberSchema, DecisionSchema, PluginSchema
from flask_httpauth import HTTPBasicAuth

api = Api(create_app())


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


class Install(Resource):
    def get(self):
        set_default_config()


api.add_resource(Install, '/install')


class CreateOrg(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('org_name', type=str, help='Name of an organization.')

    def post(self):
        args = self.parser.parse_args()
        schema = OrganizationSchema()
        org = create_org(args['org_name'])
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

    def post(self):
        args = self.parser.parse_args()
        schema = MemberSchema()
        member = create_member(args['member_name'], args['password'])
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
            'member',
            type=str,
            help='Member UUID of decision\'s author.',
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

    def post(self):
        args = self.parser.parse_args()
        du = DecisionUtils(
            title=args["title"],
            plugin=args["plugin"],
            member=args["member"],
            org=args["org"],
            directory=args["directory"]
        )
        schema = DecisionSchema()
        decision = du.create_decision()
        return schema.dumps(decision)


api.add_resource(CreateDecision, '/create/decision')


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