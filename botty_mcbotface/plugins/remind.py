import arrow
from botty_mcbotface import log
from botty_mcbotface.botty.api import get_user_name_by_id, send_user_dm
from botty_mcbotface.botty.db import db, db_create_row, db_delete_row, db_read_row, db_update_row, User
from botty_mcbotface.botty.db.models.remind import Reminder
from botty_mcbotface.task_runner import bot_routine
from slackbot.bot import listen_to, re


@bot_routine({'day_of_week': 'mon'}, cron=True, delay=False, run_once=False)
def test_remind():
    print('test-remind')


reminder_cache = []


def _load_cache():
    global reminder_cache
    reminder_cache = db.session().query(Reminder).all()
    db.session().close()


@bot_routine(0, delay=False, run_once=True)
def load_cache():
    log.info('load_cache')
    send_user_dm('U5GPFNFP0', 'hello')
    return _load_cache()


def get_user_reminders(u_id):
    """

    :param u_id:
    :return:
    """
    user = db_read_row(User, u_id)
    print('user by id: ', user.slack_name)

    reminders = user.reminders
    print('reminders by user by id: ', reminders)

    return [r.message for r in reminders]


def create_reminder(unique_id, data, text):
    db_create_row(Reminder(added_user=unique_id,
                           added_time=arrow.utcnow().datetime,
                           added_chan=data['channel'],
                           message=text,
                           remind_time=arrow.utcnow().shift(minutes=+2).datetime))


def delete_reminder():
    pass


@listen_to('^\.remind (.*)', re.IGNORECASE)
def remind(message, text):
    """

    :param message:
    :param text:
    :return:
    """
    print('REMIND')
    data = message._body
    u_id = data['user']
    u_name = get_user_name_by_id(u_id)
    unique_id = u_name + u_id

    if 'add' in text:
        create_reminder(unique_id, data, text)

    messages = get_user_reminders(unique_id)
    print([m for m in messages])
    # return message.send([r.message for r in get_reminders(unique_id)])
