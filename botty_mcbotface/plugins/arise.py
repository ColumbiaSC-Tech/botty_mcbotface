# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, re
from botty_mcbotface.utils.tools import random_response

responses = ['ugh... fine.',
             '_Up from the 36 chambers!!!!_',
             '_rubs eyes_\n ...huh?',
             ':fire::fire::fire:ᕦ໒( ᴼ 益 ᴼ )७ᕤ:fire::fire::fire:']


@respond_to('^arise|wake', re.IGNORECASE)
def arise(message):
    """
    Wake botty_mcbotface up
    :param message: Slackbot message object
    :param _:
    :return: Message to slack channel
    """
    return message.send(random_response(responses))
