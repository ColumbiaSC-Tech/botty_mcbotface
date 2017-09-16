# -*- coding: utf-8 -*-
from slackbot.bot import listen_to, re
from botty_mcbotface.utils.tools import random_response


@listen_to(r'^\\o/', re.IGNORECASE)
def cheers(message):
    """
    Returns a celebratory response to the channel
    :param message: Slackbot message object
    :return: Message to slack channel
    """
    _cheers = [
        "FUCK YEAH!",
        "CHEEEEEEEEAAAAA BOIIIIIIIII!!!!",
        "DOGGIE DOGGIE WHAT NOW?!",
        "♪  ┏(°.°)┛ GET DOWN ┗(°.°)┓ ♬"
        "GAME ON BITCHEZZZ!!",
        "GET SOME!!",
        "HOORAH!",
        "HURRAY!",
        "OORAH!",
        "OOHHHYEEEEEEEEEEEAH!",
        "YAY!",
        "*\o/* CHEERS! *\o/*",
        "HOOHAH!",
        "HOOYAH!",
        "HUAH!",
        "♪  ┏(°.°)┛  ┗(°.°)┓ ♬"
    ]
    return message.send(random_response(_cheers))
