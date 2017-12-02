from botty_mcbotface import log
from botty_mcbotface.botty.api import get_all_channels, get_all_users
from botty_mcbotface.botty.db import db_add_row, db_merge_row, Channel, User
from botty_mcbotface.tasq_runner import bot_routine


@bot_routine(3600, delay=False)
def populate_channels():
    """Retrieves all public channels for a Slack team and merges new members to Channels table."""
    log.info('populate_channels')
    chans = get_all_channels().body['channels']

    for c in chans:
        if not c['is_private']:
            db_merge_row(Channel(id=c['id'], name=c['name']))


@bot_routine(3600, delay=False)
def populate_users():
    """Retrieves all users for a Slack team and merges new members to Users table."""
    log.info('populate_users')
    users = get_all_users().body['members']

    for u in users:
        if not u['deleted']:
            s_id = u['id']
            s_name = u['name']

            # Create our custom unique user ID's (slackID + slackUserName)
            _id = s_name + s_id
            db_merge_row(User(id=_id, slack_id=s_id, slack_name=s_name))
