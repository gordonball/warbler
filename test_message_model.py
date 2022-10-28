"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from sqlite3 import IntegrityError
from unittest import TestCase
from models import db, User, Message, Follows, connect_db
from sqlalchemy import exc
from datetime import datetime
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()

class MessageModelTestCase(TestCase):
    def setUp(self):
        Message.query.delete()
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id


        m1 = Message("This is a test", datetime.now(), self.u1_id)
        m2 = Message("Test message please ignore", datetime.now(), self.u2_id)

        db.session.commit()
        self.m1_id = m1.id
        self.m2_id = m2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_message_model(self):
        u1 = User.query.get(self.u1_id)
        m1 = Message.query.get(self.m1_id)

        self.assertEqual(m1.users_liked, [])

        m1.users_liked.append(u1)

        self.assertIn(m1.users_liked, u1)

        with self.assertRaises(exc.IntegrityError):
            m1.users_liked.append(None)
            db.session.flush()
        db.session.rollback()

    def test_add_message(self):
        u1 = User.query.get(self.u1_id)

        with self.assertRaises(exc.IntegrityError):
            m1 = Message("", datetime.now(), None)
            db.sessions.flush()
        db.session.rollback()

        with self.assertRaises(exc.IntegrityError):
            m2 = Message("This is a bad time.", 4, u1.id)
            db.sessions.flush()
        db.session.rollback()



