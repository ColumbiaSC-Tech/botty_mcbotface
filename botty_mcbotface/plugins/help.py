# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, re


@respond_to('^help', re.IGNORECASE)
def love(message):
    help_msg = '\nI\'m not a very smart baht...\n' \
               'You can command me with _dot_ commands.\n' \
               'Here\'s what I know so far\n' \
               '`.g <search term>` - Search google and return the first result' \
               '`.y <search term>` - Search youtube and return the first result'
    return message.reply(help_msg)

