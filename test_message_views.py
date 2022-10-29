"""Message View tests."""

# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, Message, User, connect_db

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app, CURR_USER_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageBaseViewTestCase(TestCase):
    def setUp(self):
        #injection
        Message.query.delete()
        #end injection
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        db.session.flush()

        m1 = Message(text="m1-text", user_id=u1.id)
        db.session.add_all([m1])
        db.session.commit()

        self.u1_id = u1.id
        self.m1_id = m1.id

        self.client = app.test_client()


class MessageAddViewTestCase(MessageBaseViewTestCase):
    def test_add_message(self):
        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:
        with self.client as c: #this is a mere convenience
            with c.session_transaction() as sess: #this is a black box. kinda.
                sess[CURR_USER_KEY] = self.u1_id

            # doesn't literally work but conceptually...
            # sess = c.session_transaction()
            # sess[CURR_USER_KEY] = self.u1_id

            # ...testing...

            # finally, sess.pop(CURR_USER_KEY)

            # in other words, what is a context manager anyway?

            # Now, that session setting is saved, so we can have
            # the rest of ours test
            resp = c.post("/messages/new", data={"text": "Hello"})

            self.assertEqual(resp.status_code, 302)

            Message.query.filter_by(text="Hello").one()


    def test_delete_message(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.post(f"/messages/{self.m1_id}/delete")

            self.assertEqual(resp.status_code, 302) #this is a post redirecting you.
            #you can set follow_redirects to true and then test 200 for html. then search that html

            #in our test... test messages text body can be distinct, and
            # and then test you're on the correct page. it WAS there before. and THEN after delete it's not there.

            #why is it 302 status code, where is the api?

            test_list = Message.query.filter_by(id = self.m1_id).all()
            self.assertEqual(len(test_list), 0)
