#!/usr/bin/env python
from six.moves.urllib.parse import unquote
from slackbot.bot import listen_to, re
from ..tools import get_html
from .weather import weather_setup


@listen_to('^.g (.*)', re.IGNORECASE)
def google(message, search):
    """
    Performs a google search and returns the href of 1st result
    :param message: Slackbot message object
    :param search: User search string
    :return: Message to slack channel
    """
    search_url = 'https://www.google.com/search?q=' + search
    first_result = get_html(search_url).select('h3.r > a')

    # Skip the first link if it's a google images link
    res = first_result[1]['href'] if 'Images for ' in first_result[0] else first_result[0]['href']

    # Remove google link tracking metadata from URL
    link = re.sub(r'^/url\?q=', '', res).split('&sa=', 1)[0]

    return message.send(unquote(link))


@listen_to('^.w (\d{5})', re.IGNORECASE)
def weather(message, zip_code):
    """
    TODO: Find good weather API
    :param message:
    :param zip_code:
    :return:
    """
    res = weather_setup(zip_code)
    return message.send('Eh... I\'m workin on it')
