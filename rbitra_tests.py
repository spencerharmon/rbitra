from rbitra import create_app, db, configure
from rbitra.models import Configuration, Server, Organization, Member, MemberDigest
from rbitra.configure import set_default_config
from rbitra.schema import MemberSchema, OrganizationSchema
from werkzeug.security import check_password_hash
import unittest
import json
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


    def test_create_member(self):
        set_default_config()
        response = self.client.post(
            '/create/member',
            data={
                'member_name': "testuser",
                'password': "test123"
            }
        )
        member = Member.query.filter_by(name="testuser").first()
        digest = MemberDigest.query.filter_by(member=member.uuid).first()

        self.assert200(response)
        self.assertNotEqual(member, None)
        self.assertTrue(check_password_hash(digest.digest, "test123"))


    def test_create_decision_add_member_to_org(self):
        set_default_config()
        member_resp = self.client.post(
            '/create/member',
            data={
                'member_name': "testuser",
                'password': "test123"
            }
        )
        member = json.loads(member_resp.json)
        self.assert200(member_resp)

        org_resp = self.client.post(
            '/create/org',
            data={'org_name': "test org"}
        )
        org = json.loads(org_resp.json)
        self.assert200(org_resp)

        plugin_resp = self.client.post(
            '/install/plugin',
            data={'git_url': 'https://www.github.com/spencerharmon/meta_plugin'}
        )
        plugin = json.loads(plugin_resp.json)
        self.assert200(plugin_resp)

        response = self.client.post(
            '/create/decision',
            data={
                "title": "test decision",
                "plugin": plugin["uuid"],
                "member": member["uuid"],
                "org": org["uuid"],
                "directory": "testdecision"
            }
        )
        self.assert200(response)

if __name__ == '__main__':
    unittest.main()
