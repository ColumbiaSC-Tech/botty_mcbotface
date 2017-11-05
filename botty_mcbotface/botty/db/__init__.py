import asyncio
import concurrent.futures
import os
from botty_mcbotface.botty.api import get_all_channels, get_all_users
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Query, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from time import sleep


class BottyDB:
    """Application global database for plugin use"""

    def __init__(self):
        self.engine = create_engine('sqlite:///botty.db')
        self.factory = sessionmaker(bind=self.engine, query_cls=Query)
        self.session = scoped_session(self.factory)
        self.metadata = MetaData()
        self.base = declarative_base(metadata=self.metadata, bind=self.engine)
        self.base.query = self.session.query_property(query_cls=Query)


#####################################
#    DB Initialization Functions    #
#####################################

# FIXME: For testing only.
# Once baseline relationships are established use Alembic
db_name = 'botty.db'
if os.path.exists(db_name):
    os.remove(db_name)
    print('REMOVED::', db_name)

# Instantiate db
db = BottyDB()
Base = db.base
session = db.session

# Import models here to avoid circular importing
from botty_mcbotface.botty.db.models import *

Base.metadata.create_all(bind=db.engine)


def db_add_row(row):
    sess = db.session()
    sess.merge(row)
    sess.commit()
    sess.close()
    # sess.execute(insert(row, prefixes=['OR IGNORE']))


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


# Start an event loop for async requests
loop = asyncio.get_event_loop()


@asyncio.coroutine
def populate_periodic():
    # while True:
    print('populate_periodic::RUNNING')

    tasks = [populate_channels, populate_users]

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [loop.run_in_executor(executor, t) for t in tasks]
        yield from asyncio.gather(*futures)
        print('populate_periodic::SLEEP')
        yield from asyncio.sleep(15)
        yield from populate_periodic()


loop.run_until_complete(populate_periodic())

print('DB_INIT::finished')
# print('sleeping...')
# sleep(5)
# loop.run_until_complete(populate_periodic())
#
# populate_channels()
# populate_users()

