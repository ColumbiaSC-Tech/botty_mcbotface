#!/usr/bin/env python

from requests import request
from bs4 import BeautifulSoup
from slackbot.bot import listen_to, respond_to, re


def soup(html):
    bs = BeautifulSoup(html, 'lxml')
    return bs


def get(url):
    res = request('get', url)
    return soup(res.text)


@listen_to('^.g (.*)', re.IGNORECASE)
def google(message, search):
    """
    Performs a google search and returns the href of 1st result
    :param message: Slackbot message object
    :param search: User search string
    :return: Message to slack channel
    """
    search_url = 'https://www.google.com/search?q=' + search
    first_result = get(search_url).select('h3.r > a')[0]['href']
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
    print(zip_code)
    message.send()
