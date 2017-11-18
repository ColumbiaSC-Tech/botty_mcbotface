from botty_mcbotface.botty.db import Base
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import backref, relationship


class Reminder(Base):
    """Table for Reminder plugin (plugins/reminder.py)"""
    __tablename__ = 'reminders'

    added_user = Column(String(32), ForeignKey('users.id'), primary_key=True)
    added_time = Column(DateTime, primary_key=True)
    added_chan = Column(String(50), primary_key=True)
    message = Column(String(512))
    remind_time = Column(DateTime)

    users = relationship('User', backref=backref('reminders', cascade='all, delete-orphan'))
