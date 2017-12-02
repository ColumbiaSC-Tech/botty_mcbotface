from botty_mcbotface.utils.tools import get_html
from slackbot.bot import listen_to, re
from datetime import datetime
from pytz import timezone


@listen_to('^.today', re.IGNORECASE)
def today(message):
    """
    Returns all the holidays for today
    :param message: Slackbot message object
    :return: Message to slack channel
    """
    east_tz = timezone('US/Eastern')
    _today = datetime.now(east_tz).strftime("%A, %B %d, %Y.")
    msg = "_{}_\n*Today's Holidays:*\n".format(_today)

    holidays = get_html("https://www.checkiday.com/rss.php?tz=America/New_York").find_all('title')

    for holiday in holidays:
        if 'checkiday.com' in holiday.text.lower():
            continue
        msg += '• {}\n'.format(holiday.text)

    return message.send(msg)
