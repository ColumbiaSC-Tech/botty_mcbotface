#!/usr/bin/env python
from slackbot.bot import listen_to, respond_to, re
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
    first_result = get_html(search_url).select('h3.r > a')[0]['href']
    res = re.sub(r'^/url\?q=', '', first_result).split('&sa=', 1)[0]
    return message.send(res)


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
