import arrow
import asyncio
from botty_mcbotface.botty.api import get_user_name_by_id
from botty_mcbotface.botty.db import db, db_add_row, User
from sqlalchemy import Column, DateTime, ForeignKey, String
from slackbot.bot import listen_to, re


class Reminder(db.base):
    __tablename__ = 'reminders'

    added_user = Column(String(32), ForeignKey(User.id), primary_key=True)
    added_time = Column(DateTime, primary_key=True)
    added_chan = Column(String(50))
    message = Column(String(512))
    remind_time = Column(DateTime)


db.base.metadata.create_all(db.engine)


@listen_to('^\.remind (.*)', re.IGNORECASE)
def test_data_setup(message, text):
    u_id = message._body['user']
    u_name = get_user_name_by_id(u_id)
    unique_id = u_name + u_id

    db_add_row(Reminder(added_user=unique_id,
                        added_time=arrow.utcnow().datetime,
                        added_chan='test_chan',
                        message=text,
                        remind_time=arrow.utcnow().datetime))


# test_data_setup()
# print(session.query(User).filter(User.name == 'danny').all())
