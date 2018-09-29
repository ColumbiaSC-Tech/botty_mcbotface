from botty_mcbotface import log
from botty_mcbotface.botty.api import get_all_channels, get_all_users
from botty_mcbotface.botty.db import db_update_row, Channel, User
from botty_mcbotface.task_runner import bot_routine


HOURLY: int = 60 * 60
DAILY: int = 60 * 60 * 24


@bot_routine(DAILY, delay=15)
def populate_channels():
    """Retrieves all public channels for a Slack team and merges new members to Channels table."""
    log.info('populate_channels')
    chans = get_all_channels().body['channels']

    for c in chans:
        if not c['is_private']:
            db_update_row(Channel(id=c['id'], name=c['name']))


@bot_routine(HOURLY, delay=30)
def populate_users():
    """Retrieves all users for a Slack team and merges new members to Users table."""
    log.info('populate_users')
    users = get_all_users().body['members']

    for u in users:
        if not u['deleted']:
            s_id = u['id']
            s_name = u['name']
            is_admin = u['is_admin']
            is_owner = u['is_owner']
            # Create our custom unique user ID's (slackID + slackUserName)
            _id = s_name + s_id
            db_update_row(User(id=_id,
                               slack_id=s_id,
                               slack_name=s_name,
                               is_admin=is_admin,
                               is_owner=is_owner))
