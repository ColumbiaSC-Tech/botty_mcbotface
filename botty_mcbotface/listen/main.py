#!/usr/bin/env python

from slackbot.bot import listen_to, respond_to, re


@listen_to('Can someone help me?', re.IGNORECASE)
def help(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('Yes, I can!')

    # Message is sent on the channel
    message.send('I can help everybody!')

    # Start a thread on the original message
    message.reply("Here's a threaded reply", in_thread=True)


