class Response:
    """
    Mocked GET response for requests.get
    """
    def __init__(self, url):
        self.text = open(url)


class MockMessage:
    """
    Mocked `Message` object from slackbot.
    Passed to decorated plugin functions as first param.
    """
    def __init__(self, debug=False):
        self.debug = debug
        self._body = {'channel': '#test_channel'}

    def reply(self, text):
        if self.debug:
            print(text)

        return text

    def send(self, text):
        if self.debug:
            print(text)

        return text
