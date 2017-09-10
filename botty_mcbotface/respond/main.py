#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackbot.bot import listen_to, respond_to, re


@respond_to('^(arise|wake)', re.IGNORECASE)
def arise(message, command):
    responses = [
        '_Up from the 36 chamber!!!!_',
        ':fire::fire::fire:ᕦ໒( ᴼ 益 ᴼ )७ᕤ:fire::fire::fire:'
    ]
    return message.send(responses[1])
    # react with thumb up emoji
    # message.react('+1')


@respond_to('I love you', re.IGNORECASE)
def love(message):
    message.reply('I love you too!')

