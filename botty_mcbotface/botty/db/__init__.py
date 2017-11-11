import asyncio
import concurrent.futures
import threading
import os
from botty_mcbotface.botty.api import get_all_channels, get_all_users
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Query, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData


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
    sess.add(row)
    sess.commit()
    sess.close()
    # sess.execute(insert(row, prefixes=['OR IGNORE']))


def db_merge_row(row):
    sess = db.session()
    sess.merge(row)
    sess.commit()
    sess.close()
    # sess.execute(insert(row, prefixes=['OR IGNORE']))


def populate_channels():

    chans = get_all_channels().body['channels']

    for c in chans:
        if not c['is_private']:
            db_merge_row(Channel(id=c['id'], name=c['name']))


def populate_users():

    users = get_all_users().body['members']

    for u in users:
        if not u['deleted']:
            s_id = u['id']
            s_name = u['name']
            _id = s_name + s_id
            db_merge_row(User(id=_id, slack_id=s_id, slack_name=s_name))


@asyncio.coroutine
def populate_periodic(_loop):

    print('populate_periodic::RUNNING')

    tasks = [populate_channels, populate_users]
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks))
    # print(executor.__dict__)

    def periodic(loop):
        with executor:
            futures = [loop.run_in_executor(executor, t) for t in tasks]
            yield from asyncio.gather(*futures)
            print('populate_periodic::SLEEP')
            # TODO: Implement scheduler for this task
            # try:
            #     yield from sleep(15)
            # except Exception as e:
            #     return print('SLEEP_EXCEPTION', e)

            # yield from periodic(loop, sleep)

    yield from periodic(_loop)


def async_queue():

    # Start a new event loop for async requests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Set and start async work thread
    work = threading.Thread(target=lambda: loop.run_until_complete(populate_periodic(loop)))
    work.start()


async_queue()
print('DB_INIT::finished')
