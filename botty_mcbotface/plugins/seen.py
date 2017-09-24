from datetime import datetime

import pytz
from slackbot.bot import listen_to, re

from botty_mcbotface.botty.api import get_user_name_by_id, get_user_message_history


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

    messages = get_user_message_history(user_id)
    user_name = get_user_name_by_id(user_id)

    for msg in messages['messages']['matches']:
        if msg.keys() & {'text', 'ts'}:
            ch = msg['channel']['name']
            ts = datetime.fromtimestamp(float(msg['ts']), tz=pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M')
            m = '@{} was last seen *{}*, in #{} saying:\n> {}'.format(user_name, ts, ch, msg['text'])
            return message.send(m)

    return message.send('Yea... I can\'t go that far back in time...')
