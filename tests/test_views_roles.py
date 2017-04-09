import os
import unittest
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User, Entry, Role


#1. add new users with different roles to the blogful-test database
#2. user0 is admin, user1 doesn't have role, user 3 doesn't have role
#3. user1 adds new entry
#4. user0 tries to edit the entry, user 1 tries to edit, user3 tries to edit
#5. drop the data from all tables

class TestViews(unittest.TestCase):
    def setUp(self):
        #create users
        self.client = app.test_client()
        Base.metadata.create_all(engine)
        self.user_admin = User(name="Admin", email="admin@blogtest.com",
                               password=generate_password_hash("test"))
        self.user_editor = User(name="Editor", email="editor@blogtest.com",
                                password=generate_password_hash("test"))
        self.user_reader = User(name="Reader", email="reader@blogtest.com",
                                password=generate_password_hash("test"))
        session.add_all([self.user_admin, self.user_reader, self.user_editor])
        admin_id = session.query(User).filter_by(name="Admin").first()
        self.role_admin = Role(owner_id=admin_id.id, role_name="Admin")
        session.add(self.role_admin)
        session.commit()

    def tearDown(self):
        #drop everything
        session.close()
        Base.metadata.drop_all(engine)

    def login_admin(self):
        with self.client.session_transaction() as session:
            session["user_id"] = str(self.user_admin.id)
            session["_fresh"] = True

    def login_editor(self):
        with self.client.session_transaction() as session:
            session["user_id"] = str(self.user_editor.id)
            session["_fresh"] = True

    def login_reader(self):
        with self.client.session_transaction() as session:
            session["user_id"] = str(self.user_reader.id)
            session["_fresh"] = True

    def logout_user(self):
        with self.client.session_transaction() as session:
            session["user_id"] = str("None")
            session["_fresh"] = False

    def add_entry(self):
        self.login_editor()

        response = self.client.post("/entry/add", data={
            "title": "Test Entry",
            "content": "Test content"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.author, self.user_editor)

        self.logout_user

    def test_edit_entry_editor(self):
        self.add_entry()
        self.login_editor()
        response = self.client.post("/entry/id/1/edit", data={
            "title": "Edited Entry Title",
            "content": "Edited Entry Content"
        })


        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/entry/id/1")

        entry = session.query(Entry).first()
        self.assertEqual(entry.title, "Edited Entry Title")
        self.assertEqual(entry.content, "Edited Entry Content")


    def test_edit_entry_admin(self):
        self.add_entry()
        self.login_admin()
        response = self.client.post("/entry/id/1/edit", data={
            "title": "Edited Entry Title by admin",
            "content": "Edited Entry Content by admin"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/entry/id/1")

        entry = session.query(Entry).first()
        self.assertEqual(entry.title, "Edited Entry Title by admin")
        self.assertEqual(entry.content, "Edited Entry Content by admin")
        self.assertEqual(entry.author, self.user_editor)

    def test_edit_entry_reader(self):
        self.add_entry()
        self.login_reader()
        response = self.client.get("/entry/id/1/edit")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/page/1")







if __name__ == '__main__':
    unittest.main()
