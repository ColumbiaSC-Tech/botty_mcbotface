from pprint import pprint
from slackbot_settings import API_TOKEN
from slacker import Slacker

client = Slacker(API_TOKEN)

# *** Slacker API Methods *** #

def get_user_name_by_id(user_id):
    """
    Returns a user_name for a given user_id
    :param user_id:
    :return: user_name
    """
    return client.users.info(user_id).body['user']['name']


def get_user_presence(user_id):
    """
    Returns dict of 'presence' attributes (activity, name etc.)
    :param user_id:
    :return:
    """
    return client.users.get_presence(user_id).body
