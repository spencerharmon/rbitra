from rbitra import create_app
from flask_restful import Api, Resource, reqparse
from rbitra.configure import set_default_config
from rbitra.org_utils import create_org
from rbitra.member_utils import create_member
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
        create_org(args['org_name'])


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
        create_member(args['member_name'], args['password'])


api.add_resource(CreateMember, '/create/member')
