from slackbot.bot import listen_to, re
from datetime import datetime
import pytz

from botty_mcbotface.botty import api


@listen_to('^\.seen (.*)', re.IGNORECASE)
def seen(message, text):
    """
    Check the last time a user was seen on Slack.
    :param message: Slackbot message object
    :param text: Text to flip
    :return: Message to slack channel
    """

    # Search must be a valid Slack formatted username
    if not re.match('^<@[A-Z0-9]*>$', text.strip()):
        return message.send('Did you search with a username? (ie @botty_mcbotface)')

    start, second = text.split('<@')
    user_id = second.split('>')[0]

    all_channels = api.get_all_channels().body['channels']

    # Filter out private channels and channels the user is not a member of
    channels = [ch['name'] for ch in all_channels if ch['is_private'] is False and user_id in ch['members']]

    user_name = api.get_user_name_by_id(user_id)
    messages = api.get_user_message_history(user_name, channels)

    for msg in messages['messages']['matches']:
        ch = msg['channel']['name']
        ts = datetime.fromtimestamp(float(msg['ts']), tz=pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M')
        m = '@{} was last seen *{}*, in #{} saying:\n> {}'.format(user_name, ts, ch, msg['text'])

        return message.send(m)

    return message.send('Yea... I can\'t go that far back in time...')
