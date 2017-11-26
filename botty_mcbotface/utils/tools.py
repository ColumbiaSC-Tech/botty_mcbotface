import asyncio
import requests
import threading
from botty_mcbotface import log
from bs4 import BeautifulSoup
from random import choice


# *** Custom Threading Classes *** #
class WorkThread(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, task, daemon=False):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.task = task
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = daemon
        self.thread.start()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """ Method that runs forever """
        if not self.stopped():
            log.info('WORK_THREAD::STARTING_WORK::{}'.format(self.task))
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.task(loop))
            loop.close()
            log.info('WORK_THREAD::FINISHED_WORK::{}'.format(self.task))
            return self.stop()


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
