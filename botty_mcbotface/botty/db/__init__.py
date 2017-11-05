import os

from pprint import pprint
from .api import get_all_channels, get_all_users
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData


class BottyDB:
    """Application global database for plugin use"""

    def __init__(self):
        self.engine = create_engine('sqlite:///botty.db')
        self.factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(self.factory)
        self.metadata = MetaData()
        self.base = declarative_base(metadata=self.metadata, bind=self.engine)


db = BottyDB()
session = db.session

#####################################
#     Global Application Tables     #
#####################################


class Channel(db.base):
    __tablename__ = 'channels'

    id = Column(String(16), primary_key=True)
    name = Column(String(16), primary_key=True)


class User(db.base):
    __tablename__ = 'users'

    # Slack user ID's aren't guaranteed to be unique (for identification)
    id = Column(String(16), primary_key=True)
    slack_id = Column(String(16))
    slack_name = Column(String(16))


def db_add_row(row):
    session.add(row)
    session.commit()
    session.close()


def db_init():
    # FIXME: For testing only.
    # Once baseline relationships are established use Alembic
    db_name = 'botty.db'
    if os.path.exists(db_name):
        os.remove(db_name)
        print('Removed::', db_name)

    db.base.metadata.create_all(bind=db.engine)
    print('DB_INIT::finished')
    populate_channels()
    populate_users()


def populate_channels():
    chans = get_all_channels().body['channels']
    for c in chans:
        if not c['is_private']:
            db_add_row(Channel(id=c['id'], name=c['name']))


def populate_users():
    users = get_all_users().body['members']

    for u in users:
        if not u['deleted']:
            s_id = u['id']
            s_name = u['name']
            _id = s_name + s_id
            db_add_row(User(id=_id, slack_id=s_id, slack_name=s_name))


db_init()
