import asyncio
import concurrent.futures
from botty_mcbotface.botty.api import get_all_channels, get_all_users
from botty_mcbotface.botty.db import db_add_row, db_merge_row, Channel, User


def populate_channels():
    """Retrieves all public channels for a Slack team and merges new members to Channels table."""
    return True
    chans = get_all_channels().body['channels']

    for c in chans:
        if not c['is_private']:
            db_merge_row(Channel(id=c['id'], name=c['name']))


def populate_users():
    """Retrieves all users for a Slack team and merges new members to Users table."""
    return True
    users = get_all_users().body['members']

    for u in users:
        if not u['deleted']:
            s_id = u['id']
            s_name = u['name']

            # Create our custom unique user ID's (slackID + slackUserName)
            _id = s_name + s_id
            db_merge_row(User(id=_id, slack_id=s_id, slack_name=s_name))


# Async/MultiThread searching all channels
@asyncio.coroutine
def routine_populate_db(_loop):
    """
    Async periodic task to keep db Channels and Users tables up to date.
    :param _loop: Routine delegated asyncio event loop.
    :return:
    """
    print('routine_populate_db::RUNNING')

    tasks = [populate_channels, populate_users]
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks))

    def periodic(loop):
        with executor:
            futures = [loop.run_in_executor(executor, t) for t in tasks]
            yield from asyncio.gather(*futures)

    yield from periodic(_loop)

