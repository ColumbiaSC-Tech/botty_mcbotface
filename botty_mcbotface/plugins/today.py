from slackbot.bot import listen_to, re
from datetime import date
import feedparser


@listen_to('^.today', re.IGNORECASE)
def today(message):
    """
    Returns all the holidays for today
    :param message: Slackbot message object
    :return: Message to slack channel
    """
    today = date.today().strftime("%A, %B %d, %Y.")
    msg = "Today is {}\nToday's Holidays:\n".format(today)

    holidays = feedparser.parse("https://www.checkiday.com/rss.php?tz=America/New_York")

    for holiday in holidays.entries:
        msg += holiday.title + "\n"

    return message.send(msg)
