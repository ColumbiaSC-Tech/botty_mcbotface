from slacker import Slacker
from slackbot_settings import USER_TOKEN

# Bot API Tokens have certain limitations
# to get around that we can use the user_token
client = Slacker(USER_TOKEN)

# *** Slacker API Methods *** #


def get_user_name_by_id(user_id):
    """
    Returns a user_name for a given user_id
    :param user_id:
    :return: user_name
    """
    return client.users.info(user_id).body['user']['name']


def get_user_message_history(user_name):
    """
    Returns dict of 'presence' attributes (activity, name etc.)
    :param user_name:
    :return:
    """
    return client.search.messages('from:' + user_name, count=1, page=1).body
