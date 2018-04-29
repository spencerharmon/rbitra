from rbitra import create_app, db, configure
from rbitra.models import Configuration, Server, Organization
from rbitra.configure import set_default_config
from rbitra.org_utils import create_org
import unittest
import tempfile
from flask_testing import TestCase

class BasicIntegrationTest(TestCase):
    def create_app(self):
        return create_app(test=True)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_root_page(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_install(self):
        self.client.get('/install')
        current_config = Configuration.query.filter_by(name='current_config').first()
        self.assertEqual(current_config.any_member_may_create_orgs, True)

    def test_default_server_db_update(self):
        configure.create_local_server()
        recieved = Server.query.get(1)
        expected = {
            'id': 1,
            'fqdn': 'localhost',
            'port': 443
        }
        self.assertEqual(recieved.id, expected['id'])
        self.assertEqual(recieved.fqdn, expected['fqdn'])
        self.assertEqual(recieved.port, expected['port'])

    def test_create_org(self):
        set_default_config()
        response = self.client.post('/create/org', data={'org_name': "test org"})
        result = Organization.query.filter_by(name="test org").first()

        self.assert200(response)
        self.assertNotEqual(result, None)

    def test_create_org_default_server_failure(self):
        """
        ensure create org fails with 501 when default server not set
        """
        response = self.client.post('/create/org', data={'org_name': "test org"})
        result = Organization.query.filter_by(name="test org").first()

        self.assertEqual(response.status_code, 501)
        self.assertEqual(result, None)




if __name__ == '__main__':
    unittest.main()
