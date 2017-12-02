import os
from botty_mcbotface import log
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Query, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

DB_NAME = 'botty_db'
DB_URI = 'sqlite:///botty.db'


class BottyDB:
    """Application global database for plugin use"""

    def __init__(self):
        self.metadata = MetaData()
        self.engine = create_engine(DB_URI)
        self.factory = sessionmaker(bind=self.engine, query_cls=Query)
        self.session = scoped_session(self.factory)
        self.base = declarative_base(metadata=self.metadata, bind=self.engine)
        self.base.query = self.session.query_property(query_cls=Query)


# *** DB Initialization Functions *** #

# FIXME: For testing only.
# Once baseline relationships are established use Alembic
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    log.info('REMOVED::%s', DB_NAME)

# Instantiate db
db = BottyDB()
Base = db.base
session = db.session()

# Import models here to avoid circular importing
from botty_mcbotface.botty.db.models import *


# *** Common DB Functions *** #

def db_add_row(row):
    try:
        sess = db.session()
        sess.add(row)
        sess.commit()
        sess.close()
    except Exception as e:
        log.error('An error occurred while adding a row: %s', e)


def db_merge_row(row):
    try:
        sess = db.session()
        sess.merge(row)
        sess.commit()
        sess.close()
    except Exception as e:
        log.error('An error occurred while merging a row: %s', e)
