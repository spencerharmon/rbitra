from rbitra import create_app
from flask_restful import Api, Resource, reqparse
from rbitra.configure import set_default_config
from rbitra.org_utils import create_org


#parser = reqparse.RequestParser()
#parser.add_argument('org_name', type=str, help='Name of an organization.')


api = Api(create_app())

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


class Install(Resource):
    def get(self):
        set_default_config()


api.add_resource(Install, '/install')

#class CreateOrg(Resource):
#    args = parser.parse_args()

#    def post(self):
#        create_org(self.args['org_name'])


#api.add_resource(CreateOrg, '/create/org')
