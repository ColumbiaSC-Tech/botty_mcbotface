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
from itertools import starmap
from pprint import pprint
from typing import List

import googleapiclient.discovery_cache.base as cache
from google.oauth2 import service_account as account
from googleapiclient.discovery import build, Resource
from slackbot.bot import listen_to, re, SlackClient
from slackbot.dispatcher import Message

from botty_mcbotface import log
from botty_mcbotface.task_runner import bot_routine
from botty_mcbotface.utils.tools import random_response
from run import bot
from slackbot_settings import GOOGLE_CALENDAR


class BadRequest(Exception):
    """Custom exception for bad requests"""


class MemoryCache(cache.Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


calendar_cron: dict = GOOGLE_CALENDAR['cron']
calendar_log: str = calendar_cron['log_channel']
calendar_id: str = GOOGLE_CALENDAR['id']
date_format: str = '%A %B %d, %Y @ %I:%M%p'
credentials: str = 'google_calendar_creds.json'
scopes: List[str] = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_args: dict = {
    'calendarId': calendar_id,
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
    :param date: ISO formatted date string.
    :return: User friendly date string.
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
            return n_events if n > n_events else n
        except ValueError:
            raise BadRequest('Invalid request')

    raise BadRequest('Invalid request')


def get_google_calendar_events() -> List[dict]:
    """
    Retrieves all available google calendar events.
    :return: List of events.
    """

    # Authenticate and get calendar resource object
    creds: account.Credentials = account.Credentials.from_service_account_file(credentials)
    scoped_creds: account.Credentials = creds.with_scopes(scopes)
    service: Resource = build('calendar', 'v3', credentials=scoped_creds, cache=MemoryCache())

    # Call the Calendar API
    calendar_args['timeMin']: str = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result: dict = service.events().list(**calendar_args).execute()

    return events_result.get('items', [])


def format_event_message(event: dict, n_events: int) -> str:
    """
    Creates a human friendly formatted slack message for event data.
    :param event:
    :param n_events:
    :return: Formatted string
    """
    return (
        '{}*Name:* {}\n*When:* {}\n *Event Link: *{}'.format(
            f'*Event {i}*\n' if n_events > 1 else '\n',
            event.get('summary'),
            parse_date(event.get('start').get('dateTime')),
            re.search('External URL: (.*)\n', event.get('description')).group(1)
        )
    )


@listen_to('^\.calendar (.*)', re.IGNORECASE)
def google_calendar(message: Message, search: str):
    """
    Checks google calendar for events.
    :param message: Slackbot message object
    :param search: User search string
    :return: Message to slack channel
    """
    if not calendar_id:
        return message.reply(
            'It looks like this functionality has not yet been set up.\n' +
            'See the instructions here: https://github.com/ColumbiaSC-Tech/botty_mcbotface'
        )

    events: List[dict] = get_google_calendar_events()
    e_len: int = len(events)

    if not e_len:
        return message.send('No upcoming events found.')

    try:
        n_events: int = translate(search, e_len)
        iterable: enumerate = enumerate(events[:n_events], 1)

        return list(starmap(lambda i, event: message.send(format_event_message(event, n_events)), iterable))
    except BadRequest:
        return message.reply(random_response(error_responses))


@bot_routine(None, cron=calendar_cron['schedule'])
def google_calendar_event_cron():
    """
    Checks google calendar for events and posts to channels.
    :return:
    """
    client: SlackClient = bot._client
    events: List[dict] = get_google_calendar_events()

    e_len: int = len(events)
    if not e_len:

        msg: str = 'No events scheduled for today.'
        if calendar_log:
            return client.rtm_send_message(calendar_log, msg)

        return log.info(msg)

    return client.rtm_send_message(calendar_cron['message_channel'], format_event_message(events[0], 1))
