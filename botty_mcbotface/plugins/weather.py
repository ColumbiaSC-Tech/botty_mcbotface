from slackbot.bot import listen_to, re
from botty_mcbotface.utils.tools import get_html


# TODO: Find decent, free and keyless weather API (lol yea right)... or just scrape weather.com
def weather_setup(zip_code):
    url = 'https://weather.com/weather/tenday/l/{}:4:US'.format(zip_code)
    print(get_html(url))


@listen_to('^.w (\d{5})', re.IGNORECASE)
def weather(message, zip_code):
    """
    TODO: Find good weather API
    :param message: Slackbot message object
    :param zip_code: 5 digit zip code
    :return: Message to slack channel
    """
    res = weather_setup(zip_code)
    return message.send('Eh... I\'m workin on it')
