from botty_mcbotface.utils.tools import get_html


def weather_setup(zip_code):
    url = 'https://weather.com/weather/tenday/l/{}:4:US'.format(zip_code)
    print(get_html(url))
