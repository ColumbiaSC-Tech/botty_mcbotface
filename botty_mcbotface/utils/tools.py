from random import choice
from requests import request
from bs4 import BeautifulSoup


# *** General Methods *** #

def soup(html):
    """
    Get a BeautifulSoup object from html
    :param html: HTML string
    :return: BeautifulSoup object
    """
    bs = BeautifulSoup(html, 'lxml')
    return bs


def get_html(url):
    """
    Return a BeautifulSoup
    :param url: URL to get HTML from
    :return: HTML string
    """
    res = request('get', url)
    return soup(res.text)


def random_response(responses):
    """
    Return a random response given a list of responses
    :param responses: List of response strings
    :return: A random response string
    """
    return choice(responses)


