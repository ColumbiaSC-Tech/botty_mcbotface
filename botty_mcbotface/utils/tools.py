import logging
import requests
import threading
from random import choice
from time import sleep
from bs4 import BeautifulSoup

log = logging.getLogger()


# *** Custom Threading Class *** #
class WorkThread(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, task, daemon=False, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.task = task
        self._stop_event = threading.Event()
        thread = threading.Thread(target=self.run)
        thread.daemon = daemon
        thread.start()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """ Method that runs forever """
        while not self.stopped():
            self.task()
            print('Thread sleeping...')
            try:
                sleep(self.interval)
            except KeyboardInterrupt:
                print('Thread cancelled')
                return 0

    def run_queue(self, task_queue):
        task_queue()
        while not self.stopped():
            print('Queue thread sleeping...')
            try:
                sleep(self.interval)
            except KeyboardInterrupt:
                print('Thread cancelled')
                return 0

# class WorkThread(threading.Thread):
#     """Thread class with a stop() method. The thread itself has to check
#     regularly for the stopped() condition."""
#
#     def __init__(self, *args, **kwargs):
#         super(WorkThread, self).__init__(*args, **kwargs)
#         # self.interval = interval
#         self._stop_event = threading.Event()
#         # log.info('DAEMON::{}'.format(self.isDaemon()))
#
#     def stop(self):
#         self._stop_event.set()
#
#     def stopped(self):
#         return self._stop_event.is_set()
#
#     def run_interval(self, interval):
#         # Todo: Accept an interval
#         self.start()
#
#         while not self.stopped():
#             logging.info('IN THREAD LOOP')
#             sleep(interval)
#

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
