from datetime import datetime
from slackbot.bot import listen_to, re
from botty_mcbotface.utils.tools import get_user_name_by_id, get_user_presence


@listen_to('^\.seen (.*)', re.IGNORECASE)
def seen(message, text):
    """
    Check the last time a user was seen on Slack.
    :param message: Slackbot message object
    :param text: Text to flip
    :return: Message to slack channel
    """
    start, second = text.split('<@')
    user_id = second.split('>')[0]

    presence = get_user_presence(user_id)
    user_name = get_user_name_by_id(user_id)

    msg = 'Fix me... pleeaseee'

    # TODO: Need a better way to check last seen. Sometimes 'last_activity' is not present in return data
    if 'last_activity' in presence:
        last_seen = datetime.fromtimestamp(int(presence['last_activity'])).strftime('%Y-%m-%d %H:%M:%S')
        msg = user_name + ' was last seen on ' + last_seen

    return message.send(msg)
