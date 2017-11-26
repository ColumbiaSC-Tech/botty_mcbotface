import asyncio
import requests
import threading
from botty_mcbotface import log
from bs4 import BeautifulSoup
from random import choice


# *** Custom Threading Classes *** #

class AsyncWorkThread(object):
    """
    Custom Thread class that accepts functions to run async in
    event loop in a new thread.

    This thread has only one job (to run the given task) and is
    then managed by APScheduler parent thread.
    """
    def __init__(self, task, daemon=False):
        """
        :param task: Properly formatted routine to run async in thread.
        :param daemon: Boolean indicating the worker thread is daemon or not.
        """
        self.thread = threading.Thread(target=self.run, args=(task,), daemon=daemon)
        self.thread.daemon = daemon
        self.thread.start()

    @staticmethod
    def run(task):
        """
        Set, start then close the async task event loop.
        :param task: Task to run
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(task(loop))
        loop.close()


# *** General Helper Functions *** #

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
    res = requests.get(url)
    s = soup(res.text)

    return s


def random_response(responses):
    """
    Return a random response given a list of responses
    :param responses: List of response strings
    :return: A random response string
    """
    def test_1d(res):

        if isinstance(res, list):
            # Currently don't support random on nested data structures
            return True if True not in [isinstance(r, (list or set or tuple)) for r in res] else False

        return False

    if test_1d(responses):
        return choice(responses)

    raise TypeError
