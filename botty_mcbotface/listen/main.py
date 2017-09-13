#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackbot.bot import listen_to, respond_to, re
from ..tools import random_response


@listen_to('Can someone help me?', re.IGNORECASE)
def help(message):
    # Message is replied to the sender (prefixed with @user)
    return message.reply('At this point... all I can offer is my loyalty')

    # Message is sent on the channel
    # message.send('I can help everybody!')

    # Start a thread on the original message
    # message.reply("Here's a threaded reply", in_thread=True)


@listen_to(r'^\\o/', re.IGNORECASE)
def cheers(message):
    _cheers = [
        "FUCK YEAH!",
        "HOORAH!",
        "HURRAY!",
        "OORAH!",
        "YAY!",
        "*\o/* CHEERS! *\o/*",
        "HOOHAH!",
        "HOOYAH!",
        "HUAH!",
        "♪  ┏(°.°)┛  ┗(°.°)┓ ♬"
    ]
    return message.send(random_response(_cheers))
