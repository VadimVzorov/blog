from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import app
#anything inside __init__ can be accessed like that

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

import datetime

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))

from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    entries = relationship("Entry", backref="author")
    roles = relationship("Role", backref="roles")


    # def __rre
    def __str__(self):
        return "Name: {}, Roles: {}".format(self.name, [role.role_name for role in self.roles])

class Role(Base):
    __tablename__="roles"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(128))
    owner_id = Column(Integer, ForeignKey('users.id'))

# class Role(Base):
#     __tablename__ = 'roles'
#
#     id = Column(Integer, primary_key=True)
#     name.....
#
#     def __init__(self, roles=None):
#          # Do your user init
#          UserMixin.__init__(self, roles)



Base.metadata.create_all(engine)
