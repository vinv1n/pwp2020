import unittest
import logging

from flask import Flask

from api import create_app

# sources for this test
# https://julien.danjou.info/db-integration-testing-strategies-python/
# https://stackoverflow.com/questions/17791571/how-can-i-test-a-flask-application-which-uses-sqlalchemy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseTest(unittest.TestCase):

    app, db = create_app()

    def setUp(self):
        with self.app.context():
            self.db.create_all()
            self.populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
