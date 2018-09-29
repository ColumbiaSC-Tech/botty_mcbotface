# This functionality was incredibly annoying to figure out.
# Google docs have barely covered the python library that ISN'T deprecated, among other poorly and undocumented things:
#
# Here's how to do it:
#
# 1. Create a service in your google developer account for the bot.
# 2. Enable the DOMAIN-WIDE permissions for the service, then download the credentials for said service.
# 3. Rename the credential file to "google_calendar_creds.json" and place it in the root directory.
# 4. Find ID for your Google calendar and assign it to the GOOGLE_CALENDAR config variable in "slackbot_settings.py"

import datetime
import googleapiclient.discovery_cache.base as cache
from botty_mcbotface.utils.tools import random_response
from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account as account
from itertools import starmap
from slackbot_settings import GOOGLE_CALENDAR
from slackbot.dispatcher import Message
from slackbot.bot import listen_to, re
from typing import List
from pprint import pprint


class BadRequest(Exception):
    """Custom exception for bad requests"""


class MemoryCache(cache.Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


date_format: str = '%A %B %d, %Y @ %I:%M%p'
credentials: str = 'google_calendar_creds.json'
scopes: List[str] = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_args: dict = {
    'calendarId': GOOGLE_CALENDAR,
    'maxResults': 100,
    'singleEvents': True,
    'orderBy': 'startTime'
}
error_responses: List[str] = [
    'I\'m sorry I didn\'t get that...',
    'Something was wrong in that request...',
    'Are you using the syntax `.calendar next <number>`?'
]


def parse_date(date: str) -> str:
    """
    Helper for parsing ISO date string to more friendly form.
    :param date:
    :return:
    """
    return datetime.datetime.fromisoformat(date).strftime(date_format)


def translate(search: str, n_events: int) -> int:
    """
    Converts the user entered string to a number for events.
    :param search: User input.
    :param n_events: Number of available events.
    :return: The number of events to slice from event list.
    """
    s: str = search.strip()

    if s == 'next':
        return 1
    elif re.match('next \d', s):
        try:
            n: int = int(s.split('next ')[1])
            print('n::', n)
            return n_events if n > n_events else n
        except ValueError:
            raise BadRequest('Invalid request')

    raise BadRequest('Invalid request')


@listen_to('^\.calendar (.*)', re.IGNORECASE)
def google_calendar(message: Message, search: str):
    """
    Checks google calendar for events.
    :param message: Slackbot message object
    :param search: User search string
    :return: Message to slack channel
    """

    # Authenticate and get calendar resource object
    creds: account.Credentials = account.Credentials.from_service_account_file(credentials)
    scoped_creds: account.Credentials = creds.with_scopes(scopes)
    service: Resource = build('calendar', 'v3', credentials=scoped_creds, cache=MemoryCache())

    # Call the Calendar API
    calendar_args['timeMin']: str = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result: dict = service.events().list(**calendar_args).execute()
    events_items: List[dict] = events_result.get('items', [])

    if not len(events_items):
        print('No upcoming events found.')

    try:
        n_events: int = translate(search, len(events_items))
        iterable: enumerate = enumerate(events_items[:n_events], 1)

        return list(starmap(lambda i, event:
                            message.send(
                                '{}*Event:* {}\n*Starts:* {}\n *Event Link: *{}'.format(
                                    f'{i}.\n' if n_events > 1 else '\n',
                                    event['summary'],
                                    parse_date(event['start']['dateTime']),
                                    re.search('External URL: (.*)\n', event['description']).group(1)
                                )
                            ), iterable))
    except BadRequest:
        return message.reply(random_response(error_responses))
