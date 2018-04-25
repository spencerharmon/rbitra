from rbitra import create_app, db
from rbitra.models import Configuration
from flask_restful import Resource, Api
from rbitra.configure import set_default_config
import unittest
from rbitra_tests import BasicIntegrationTest

api = Api(create_app())

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

class Install(Resource):
    def get(self):
        set_default_config()

api.add_resource(Install, '/install')

class ApiTest(BasicIntegrationTest):
    def test_install(self):
        current_config = Configuration.query.filter_by(config_name='current_config').first()
        self.assertEqual(current_config['any_member_may_create_orgs'], True)

if __name__ == '__main__':
    unittest.main()