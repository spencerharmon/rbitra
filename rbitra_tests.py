from rbitra import create_app, db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rbitra.models import Configuration
from flask_migrate import init, migrate, upgrade
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
        #current_config = Configuration.query.all()
        current_config = Configuration.query.filter_by(name='current_config').first()
        self.assertEqual(current_config.any_member_may_create_orgs, True)

if __name__ == '__main__':
    unittest.main()
