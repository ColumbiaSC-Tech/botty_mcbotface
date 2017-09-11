#!/usr/bin/env python
# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, re
from ..tools import random_response


@respond_to('^(arise|wake)', re.IGNORECASE)
def arise(message, command):
    # message.react('+1')
    responses = [
        '_Up from the 36 chambers!!!!_',
        '_rubs eyes_\n ...huh?',
        ':fire::fire::fire:ᕦ໒( ᴼ 益 ᴼ )७ᕤ:fire::fire::fire:'
    ]
    return message.send(random_response(responses))


@respond_to('^help', re.IGNORECASE)
def love(message):
    help_msg = '\nI\'m not a very smart baht...\n' \
               'You can command me with _dot_ commands.\n' \
               'Here\'s what I know so far\n' \
               '`.g <search term>` - Search google and return the first result'
    return message.reply(help_msg)

