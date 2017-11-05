from botty_mcbotface.botty.db import Base
from sqlalchemy import Column, String

#####################################
#     Global Application Tables     #
#####################################


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(String(16), primary_key=True)
    name = Column(String(16), primary_key=True)


class User(Base):
    __tablename__ = 'users'

    # Slack user ID's aren't guaranteed to be unique for identification.
    # Format used is slack_name + slack_id (i.e. 'dannyU87GH7A' ).
    id = Column(String(16), primary_key=True)
    slack_id = Column(String(16))
    slack_name = Column(String(16))

