"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, User, Message, Follows, connect_db
from sqlalchemy import exc
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


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_user_repr(self):
        """TODO: make docstrings for test fn also!!"""

        u1 = User.query.get(self.u1_id)
        test_repr = u1.__repr__()

        self.assertEqual(test_repr, f"<User #{u1.id}: {u1.username}, {u1.email}>")

    def test_user_is_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_followed_by(u1))

        u1.following.append(u2)

        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2.is_followed_by(u1))

    def test_user_signup(self):

        with self.assertRaises(exc.IntegrityError):
            User.signup("u3", None, "password", None)
            db.session.flush()

        db.session.rollback()

        # TODO: testing duplicate username. separate fn!
        with self.assertRaises(exc.IntegrityError):
            User.signup("u1", "email@email.com","password", "")
            db.session.flush()

        db.session.rollback()

    def test_user_authenticate(self):

        u1_auth = User.authenticate("u1", "password"),
        u1 = User.query.get(self.u1_id)
        self.assertEqual(u1, u1_auth)

        # break these out! positive vs negative tests.
        # the more test fn's the better.
        self.assertFalse(User.authenticate("u1", ""))
        self.assertFalse(User.authenticate("", "password"))

    # def test_login_pos_1
    # def test_login_invalid_username...
    # def test_login_email... etc.
    # def test_login_pos_3
