import arrow
import asyncio
from botty_mcbotface.botty.api import get_user_name_by_id
from botty_mcbotface.botty.db import db, db_add_row, User
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from slackbot.bot import listen_to, re


class Reminder(db.base):
    __tablename__ = 'reminders'

    added_user = Column(String(32), ForeignKey(User.id), primary_key=True)
    added_time = Column(DateTime, primary_key=True)
    added_chan = Column(String(50))
    message = Column(String(512))
    remind_time = Column(DateTime)

    users = relationship('User', back_populates='reminders', cascade="all, delete-orphan", single_parent=True)


User.reminders = relationship('Reminder', back_populates='users', cascade="all, delete-orphan")
# db.base.metadata.create_all(db.engine)
Reminder.__table__.create(db.engine)


def get_reminders(u_id):
    reminders = db.session.query(Reminder).filter(Reminder.added_user == u_id).all()
    return reminders


@listen_to('^\.remind (.*)', re.IGNORECASE)
def remind(message, text):
    data = message._body
    u_id = data['user']
    u_name = get_user_name_by_id(u_id)
    unique_id = u_name + u_id

    db_add_row(Reminder(added_user=unique_id,
                        added_time=arrow.utcnow().datetime,
                        added_chan=data['channel'],
                        message=text,
                        remind_time=arrow.utcnow().datetime))
    print([r.message for r in get_reminders(unique_id)])


db_add_row(Reminder(added_user='nulleffortU5GPFNFP0',
                    added_time=arrow.utcnow().datetime,
                    added_chan='test_chan',
                    message='hard-coded reminder',
                    remind_time=arrow.utcnow().datetime))

