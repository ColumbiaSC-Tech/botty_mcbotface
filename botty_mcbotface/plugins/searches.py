from botty_mcbotface.utils.tools import get_html
from six.moves.urllib.parse import unquote
from slackbot.bot import listen_to, re
import urllib.parse

google_base_url = 'https://www.google.com/search?q='
youtube_base_url = 'https://www.youtube.com/results?search_query='


@listen_to('^\.g (.*)', re.IGNORECASE)
def google(message, search):
    """
    Performs a google search and returns the href of 1st result
    :param message: Slackbot message object
    :param search: User search string
    :return: Message to slack channel
    """

    search_url = google_base_url + urllib.parse.quote_plus(search)
    results = get_html(search_url).select('div.g h3.r a')

    # Indicators for google search links
    g_link_test = re.compile(r'/search\?q=')

    try:
        # Skip the first link if it's a google search link (images, news etc)
        first_result = next(l for l in results if not re.search(g_link_test, str(l)))

        # Remove google link tracking metadata from URL
        link = re.sub(r'^/url\?q=', '', first_result['href']).split('&sa=', 1)[0]

        return message.send(unquote(link))

    except StopIteration:
        return message.send('No Google results for that search... sorry :/')


@listen_to('^\.y (.*)', re.IGNORECASE)
def youtube(message, search):
    """
    Performs a youtube search and returns 1st result
    :param message: Slackbot message object
    :param search: User search string
    :return: Message to slack channel
    """
    search_url = youtube_base_url + search
    results = get_html(search_url).select('a.yt-uix-sessionlink')

    try:

        # YouTube html is funky when using HTTP request. Have to wrangle it a little to get the video links
        first_result = next(l for l in results if l['href'].startswith('/watch?v='))
        link = 'https://www.youtube.com' + first_result['href']

    except StopIteration:
        return message.send('No YouTube results for that search... sorry :/')

    return message.send(unquote(link))
