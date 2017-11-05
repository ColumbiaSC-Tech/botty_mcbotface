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

    users = relationship(User, backref='reminders')


Reminder.__table__.create(db.engine)

db_add_row(Reminder(added_user='nulleffortU5GPFNFP0',
                    added_time=arrow.utcnow().datetime,
                    added_chan='test_chan',
                    message='hard-coded reminder',
                    remind_time=arrow.utcnow().datetime))


def get_reminders(u_id):
    """

    :param u_id:
    :return:
    """
    user = db.session.query(User).get(u_id)
    print('user by id: ', user.slack_name)

    reminders = user.reminders
    print('reminders by user by id: ', reminders)

    return [r.message for r in reminders]


@listen_to('^\.remind (.*)', re.IGNORECASE)
def remind(message, text):
    """

    :param message:
    :param text:
    :return:
    """
    data = message._body
    u_id = data['user']
    u_name = get_user_name_by_id(u_id)
    unique_id = u_name + u_id

    db_add_row(Reminder(added_user=unique_id,
                        added_time=arrow.utcnow().datetime,
                        added_chan=data['channel'],
                        message=text,
                        remind_time=arrow.utcnow().datetime))

    messages = get_reminders(unique_id)
    print([m for m in messages])
    # return message.send([r.message for r in get_reminders(unique_id)])
