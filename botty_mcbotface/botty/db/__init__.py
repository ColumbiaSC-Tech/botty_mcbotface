import os
from botty_mcbotface import log
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


# *** DB Initialization Functions *** #

# FIXME: For testing only.
# Once baseline relationships are established use Alembic
db_name = 'botty.db'
if os.path.exists(db_name):
    os.remove(db_name)
    log.info('REMOVED::%s', db_name)

# Instantiate db
db = BottyDB()
Base = db.base
session = db.session()

# Import models here to avoid circular importing
from botty_mcbotface.botty.db.models import *


# *** Common DB Functions *** #

def db_add_row(row):
    sess = db.session()
    sess.add(row)
    sess.commit()
    sess.close()


def db_merge_row(row):
    sess = db.session()
    sess.merge(row)
    sess.commit()
    sess.close()
