from slacker import Slacker
from slackbot_settings import USER_TOKEN
import re

# Bot API Tokens have certain limitations
# to get around that we can use the user_token
client = Slacker(USER_TOKEN)

# Regular expressions for sanitizing Slack formatted input strings
re_chan = re.compile(r'<#[A-Z0-9]*\|[^>]*>')
re_link = re.compile(r'<https?://[^|]*\|[^>]*>')
re_user = re.compile(r'<@[A-Z0-9]*>')


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


def sanitize_chan_str(txt, match):
    """
    Sanitizes channel formatted Slack input strings
    (<#chan-name> => #chan-name)
    :param txt: Slack input string
    :param match: Regex found match to replace
    :return:
    """

    # Extract the channel name from surrounding chars
    start, second = re.split('<#[A-Z0-9]*\|', match)
    channel_name = '#' + second.split('>')[0]

    return re.sub(re_chan, channel_name, txt, 1)


def sanitize_link_str(txt, match):
    """
    Sanitizes link formatted Slack input strings
    (<http://slack.com|slack.com> => slack.com)
    :param txt: Slack input string
    :param match: Regex found match to replace
    :return:
    """

    # Extract the link from surrounding chars
    start, second = re.split('<https?://[^|]*\|', match)
    link = second.split('>')[0]

    return re.sub(re_link, link, txt, 1)


def sanitize_user_str(txt, match):
    """
    Sanitizes user-name formatted Slack input strings (userIDs)
    (<@IU43HD933> => @username)
    :param txt: Slack input string
    :param match: Regex found match to replace
    :return:
    """
    # Extract the id from surrounding chars
    start, second = match.split('<@')
    user_id, end = second.split('>')

    # Query the Slack API then piece it all back together
    user_name = '@' + get_user_name_by_id(user_id)

    return re.sub(match, user_name, txt)


def sanitize_slack_str(text):
    """
    Catch all function for parsing input strings
    and replacing Slack formatting
    :param text: Slack input string
    :return: text
    """
    # Map regex to their associated sanitizing fn's
    re_to_san = {re_chan: sanitize_chan_str,
                 re_link: sanitize_link_str,
                 re_user: sanitize_user_str}

    # Loop through Mapping, search for regex matches in text, call san fn's as needed
    for r in re_to_san.keys():
        if re.search(r, text):
            matches = re.findall(r, text)
            for match in matches:
                text = re_to_san[r](text, match)

    return text

