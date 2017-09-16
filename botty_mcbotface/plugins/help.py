# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, re


@respond_to(r'^halp|help', re.IGNORECASE)
def help_bot(message):
    help_msg = '\nI\'m not a very smart baht...\n' \
               'You can command me with _dot_ commands.\n' \
               'Here\'s what I know so far\n' \
               '`.(8|8ball|eightball) <question>` - Ask the magic 8ball a question\n' \
               '`.fix table(s)` - I can flip tables right side up\n' \
               '`.flip table(s)` - I can flip tables upside down\n' \
               '`.flip <word>` - I can flip words upside down\n' \
               '`.seen <@user>` - Checks the last time a user was on Slack\n' \
               '`.today` - Returns all the holidays for today\n' \
               '`.g <search term>` - Search google and return the first result\n' \
               '`.y <search term>` - Search youtube and return the first result'
    return message.reply(help_msg)

