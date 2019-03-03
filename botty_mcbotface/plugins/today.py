from datetime import datetime

from slackbot.bot import listen_to, re

from botty_mcbotface import bot_tz
from botty_mcbotface.utils.tools import get_xml


@listen_to('^.today', re.IGNORECASE)
def today(message):
    """
    Returns all the holidays for today
    :param message: Slackbot message object
    :return: Message to slack channel
    """
    _today = datetime.now(bot_tz).strftime("%A, %B %d, %Y.")
    msg = "_{}_\n*Today's Holidays:*\n".format(_today)

    holidays = get_xml("https://www.checkiday.com/rss.php?tz=America/New_York").find_all('title')

    for holiday in holidays:
        if 'checkiday.com' in holiday.text.lower():
            continue
        msg += '• {}\n'.format(holiday.text)

    return message.send(msg)
