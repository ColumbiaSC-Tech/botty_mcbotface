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
from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account as account
from slackbot.bot import listen_to, re
from typing import List
from pprint import pprint


class MemoryCache(cache.Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


credentials: str = 'google_calendar_creds.json'
scopes: List[str] = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_args: dict = {
    'calendarId': 'pk2pnrh8sj16dr6cquv37mc7sk@group.calendar.google.com',
    'maxResults': 100,
    'singleEvents': True,
    'orderBy': 'startTime'
}


@listen_to('^\.calendar (.*)', re.IGNORECASE)
def google_calendar(message, search):
    """
    Checks google calendar for events.
    :param message: Slackbot message object
    :param search: User search string
    :return: Message to slack channel
    """
    # TODO: FIX DELAY IN ROUTINES
    creds: account.Credentials = account.Credentials.from_service_account_file(credentials)
    scoped_creds: account.Credentials = creds.with_scopes(scopes)
    service: Resource = build('calendar', 'v3', credentials=scoped_creds, cache=MemoryCache())

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat()  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(**calendar_args).execute()
    events = events_result.get('items', [])

    all_events = [event for event in events]

    if not len(events):
        print('No upcoming events found.')

    pprint(all_events)

    # start = event['start'].get('dateTime', event['start'].get('date'))
    # print(start, event['summary'])
