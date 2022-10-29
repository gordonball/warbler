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

        m1 = Message(
            text = "This is a test",
            timestamp = datetime.now(),
            user_id = self.u1_id
        )
        m2 = Message(
            text = "Test message please ignore",
            timestamp = datetime.now(),
            user_id = self.u2_id
        )

        db.session.add(m1)
        db.session.add(m2)
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

        self.assertIn(u1, m1.users_liked)

        # TODO:
        # with self.assertRaises(exc.IntegrityError):
        #     m1.users_liked.append('1') NOTE: this conflicts with db models! so that's why no integrity error.

        #     bad_like = Like(user_id = , message_id = )
        #     session add
        #     session flush (NOTE: something like this for liking twice etc)

        #     db.session.add()
        #     db.session.flush()
        # db.session.rollback()

    def test_add_message(self):
        u1 = User.query.get(self.u1_id)

        with self.assertRaises(exc.IntegrityError):
            m1 = Message(
                text = "",
                timestamp = datetime.now(),
                user_id = None
            )
            db.session.add(m1)
            db.session.flush()
        db.session.rollback()

        #TODO: ProgrammingError? is psql sassing me?
        with self.assertRaises(exc.ProgrammingError):
            m2 = Message(
                text = "This is a bad time.",
                timestamp = 4, # <---- bad datatype. not a great test.
                user_id = u1.id
            )
            db.session.add(m2)
            db.session.flush()
        db.session.rollback()

        # violating referrential integrity, and also other stuff. is what IntegrityError means.
        # TODO: also test a good case!
