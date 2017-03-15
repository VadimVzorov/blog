import os
from flask_script import Manager
from blog.database import session, Entry

from blog import app

manager = Manager(app)

@manager.command
def run():
    app.run()

@manager.command
def seed():
    content = "Test content"

    for i in range(25):
        entry = Entry(
            title = "test entry#{}".format(i),
            content = content
        )
        session.add(entry)
    session.commit()

if __name__ == "__main__":
    manager.run()
