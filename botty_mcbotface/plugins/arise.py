# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, re
from botty_mcbotface.utils.tools import random_response


@respond_to('^(arise|wake)', re.IGNORECASE)
def arise(message, command):
    # message.react('+1')
    responses = [
        '_Up from the 36 chambers!!!!_',
        '_rubs eyes_\n ...huh?',
        ':fire::fire::fire:ᕦ໒( ᴼ 益 ᴼ )७ᕤ:fire::fire::fire:'
    ]
    return message.send(random_response(responses))
