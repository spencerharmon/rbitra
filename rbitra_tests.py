from rbitra import create_app, db, configure
from rbitra.models import Configuration, Server, Organization, Member, MemberDigest
from rbitra.configure import set_config
from rbitra.schema import MemberSchema, OrganizationSchema
from werkzeug.security import check_password_hash
import unittest
import json
import base64
import tempfile
from shutil import rmtree
from flask_testing import TestCase


class BasicIntegrationTest(TestCase):
    def create_app(self):
        self.app = create_app(test=True)
        return self.app

    def setUp(self):
        self.member_data = {
                'member_name': "testuser",
                'email': "test@example.com",
                'password': "test123"
            }
        self.valid_credentials = base64.b64encode(b'test@example.com:test123').decode('utf-8')
        db.create_all()

    def tearDown(self):
        rmtree(self.app.config['RBITRA_PLUGINS_PATH'], ignore_errors=True)
        rmtree(self.app.config['RBITRA_DECISION_PATH'], ignore_errors=True)
        db.session.remove()
        db.drop_all()

    def test_install(self):
        self.client.get('/install')
        current_config = Configuration.query.filter_by(name='current_config').first()
        self.assertEqual(current_config.any_member_may_create_orgs, True)

    def test_create_org(self):
        set_config()
        m_result = self.client.post(
            '/create/member',
            data=self.member_data
        )
        self.assert200(m_result)
        response = self.client.post(
            '/create/org',
            data={'org_name': "test org"},
            headers={'Authorization': 'Basic ' + self.valid_credentials}
        )
        result = Organization.query.filter_by(name="test org").first()

        self.assert200(response)
        self.assertNotEqual(result, None)

    def test_create_member(self):
        set_config()
        response = self.client.post(
            '/create/member',
            data=self.member_data
        )
        member = Member.query.filter_by(name="testuser").first()
        digest = MemberDigest.query.filter_by(member=member.uuid).first()

        self.assert200(response)
        self.assertNotEqual(member, None)
        self.assertTrue(check_password_hash(digest.digest, "test123"))

    def test_create_decision_add_member_to_org(self):
        set_config()
        member_resp = self.client.post(
            '/create/member',
            data=self.member_data
        )
        member = json.loads(member_resp.json)
        self.assert200(member_resp)

        org_resp = self.client.post(
            '/create/org',
            data={'org_name': "test org"},
            headers={'Authorization': 'Basic ' + self.valid_credentials}
        )
        org = json.loads(org_resp.json)
        self.assert200(org_resp)

        plugin_resp = self.client.post(
            '/install/plugin',
            data={'git_url': 'https://www.github.com/spencerharmon/meta_plugin'}
        )
        plugin = json.loads(plugin_resp.json)
        self.assert200(plugin_resp)

        valid_actions_resp = self.client.get(
            '/plugin/{}/valid_actions'.format(plugin["title"])
        )

        action_member_data = {
                'member_name': "actionjackson",
                'email': "aj@example.com",
                'password': "321tset"
            }
        action_member_resp = self.client.post(
            '/create/member',
            data=action_member_data
        )

        action_member = json.loads(action_member_resp.json)
        self.assert200(action_member_resp)

        actions = {}
        valid_actions = json.loads(valid_actions_resp.json)
        for k, v in valid_actions.items():
            # {'add_member_to_org': {'member': <str:uuid>, 'org': <str:uuid>}}
            actions[k] = {v['argument_keys_list'][0]: action_member['uuid'], v['argument_keys_list'][1]: org['uuid']}

        list_policies_resp = self.client.get(
            '/list/policies',
            headers={'Authorization': 'Basic ' + self.valid_credentials},
            data={'org': org['uuid']}
        )
        policy_list = list_policies_resp.json
        decision_resp = self.client.post(
            '/create/decision',
            headers={'Authorization': 'Basic ' + self.valid_credentials},
            data={
                'title': "test decision",
                'plugin': plugin["uuid"],
                'member': member["uuid"],
                'org': org["uuid"],
                'directory': "testdecision",
                'policy': policy_list[1],
                'actions': json.dumps(actions) #todo: this was passing json: why?
            }
        )
        self.assert200(decision_resp)

        approval_resp = self.client.post(
            '/approve/decision',
            headers={'Authorization': 'Basic ' + self.valid_credentials},
            data={
                'decision': json.loads(decision_resp.json)['uuid']
            }
        )
        self.assert200(approval_resp)


if __name__ == '__main__':
    unittest.main()
