# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, re

help_msg = '\nI\'m not a very smart baht...\n' \
           'You can command me with _dot_ commands.\n' \
           'Here\'s what I know so far\n' \
           '`.(8|8ball|eightball) <question>` - Ask the magic 8ball a question\n' \
           '`.calendar next <number>` - Fetch upcoming events on the CSC-Tech google calendar\n' \
           '`.fix table(s)` - Flip tables right side up\n' \
           '`.flip table(s)` - Flip tables upside down\n' \
           '`.flip <word>` - Flip words upside down\n' \
           '`.seen <@user>` - Checks the last time a user was on Slack\n' \
           '`.today` - Returns all the holidays for today\n' \
           '`.g <search term>` - Search google and return the first result\n' \
           '`.y <search term>` - Search youtube and return the first result'


@respond_to(r'^halp|help', re.IGNORECASE)
def help(message):
    """
    List botty's current commands
    :param message: Message to bot requesting help
    :return: Message to user
    """
    return message.reply(help_msg)

