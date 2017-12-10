import os
from botty_mcbotface import log
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Query, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

DB_NAME = 'botty_db'
DB_URI = 'sqlite:///botty_db'


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
# if os.path.exists(DB_NAME):
#     os.remove(DB_NAME)
#     log.info('REMOVED::%s', DB_NAME)

# Instantiate db
db = BottyDB()
Base = db.base
# session = db.session()

# Import models here to avoid circular importing
from botty_mcbotface.botty.db.models import *


# *** Common DB Functions *** #

def db_create_row(row):
    try:
        # sess = db.session()
        db.session().add(row)
        db.session().commit()
        db.session().close()
    except Exception as e:
        db.session().rollback()
        log.error('An error occurred while adding row: %s', e)


def db_read_row(table, row):
    return db.session().query(table).get(row)


def db_update_row(row):
    try:
        # sess = db.session()
        db.session().merge(row)
        db.session().commit()
        db.session().close()
    except Exception as e:
        db.session().rollback()
        log.error('An error occurred while merging row: %s', e)


def db_delete_row(row):
    try:
        # sess = db.session()
        db.session().delete(row)
        db.session().commit()
        db.session().close()
    except Exception as e:
        db.session().rollback()
        log.error('An error occurred while deleting row: %s', e)
