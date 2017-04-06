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

from getpass import getpass

from werkzeug.security import generate_password_hash

from blog.database import User

@manager.command
def adduser():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()

from blog.database import Role

@manager.command
def createroles():
    email = input("email: ")
    role = input("role: ")
    new_role = Role(role_name=role)
    user = session.query(User).filter_by(email=email).first()
    if user:
        user.roles.append(new_role)
        session.commit()
        print('role was added')
    else:
        print('no such user')


# from flask_permissions.models import Role
#
# @manager.command
# def addroles():
#     import pdb; pdb.set_trace()
#     admin = Role("admin")
#     admin.add_abilities("edit", "delete", "read")
#     session.add(admin)
#     session.commit()

from flask_migrate import Migrate, MigrateCommand
from blog.database import Base

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
