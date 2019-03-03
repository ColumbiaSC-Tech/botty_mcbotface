from random import choice

import requests
from bs4 import BeautifulSoup


# *** General Helper Functions *** #

def soup(html: str, doc_type: str = "lxml"):
    """
    Get a BeautifulSoup object from html
    :param html: HTML string
    :param doc_type: Document type
    :return: BeautifulSoup object.
    """
    bs = BeautifulSoup(html, doc_type)

    return bs


def get_html(url):
    """
    Return a BeautifulSoup
    :param url: URL to get HTML from
    :return: HTML of requested URL.
    """
    res = requests.get(url)
    s = soup(res.text)

    return s


def get_xml(url):
    """
    Return a BeautifulSoup
    :param url: URL to get XML from
    :return: XML of requested URL.
    """
    res = requests.get(url)
    s = soup(res.text, "lxml-xml")

    return s


def random_response(responses):
    """
    Return a random response given a list of responses
    :param responses: List of response strings
    :return: A random response string.
    """

    def test_1d(res):

        if isinstance(res, list):
            # Currently don't support random on nested data structures
            return True if True not in [isinstance(r, (list or set or tuple)) for r in res] else False

        return False

    if test_1d(responses):
        return choice(responses)

    raise TypeError
