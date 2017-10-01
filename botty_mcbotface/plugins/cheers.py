# -*- coding: utf-8 -*-
from slackbot.bot import listen_to, re
from botty_mcbotface.utils.tools import random_response

responses = ["UNNNNNHHH NA NA NA NAA!!!!!!",
             "CHEEEEEEEEAAAAA BOIIIIIIIII!!!!",
             "DOGGIE DOGGIE WHAT NOW?!",
             "♪  ┏(°.°)┛ GET DOWN ┗(°.°)┓ ♬",
             "GAME ON!!!!",
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
             "WOOT!!",
             "WHOOP WHOOP!!",
             "♪  ┏(°.°)┛  ┗(°.°)┓ ♬"]


@listen_to(r'^\\o/', re.IGNORECASE)
def cheers(message):
    """
    Returns a celebratory response to the channel
    :param message: Slackbot message object
    :return: Message to slack channel
    """
    return message.send(random_response(responses))
