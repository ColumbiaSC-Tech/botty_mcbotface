# -*- coding: utf-8 -*-

import random
from collections import defaultdict
from slackbot.bot import listen_to, re
from botty_mcbotface.utils import formatting

table_status = defaultdict(lambda: None)

replacements = {'a': 'ɐ',
                'b': 'q',
                'c': 'ɔ',
                'd': 'p',
                'e': 'ǝ',
                'f': 'ɟ',
                'g': 'ƃ',
                'h': 'ɥ',
                'i': 'ᴉ',
                'j': 'ɾ',
                'k': 'ʞ',
                'l': 'ן',
                'm': 'ɯ',
                'n': 'u',
                'o': 'o',
                'p': 'd',
                'q': 'b',
                'r': 'ɹ',
                's': 's',
                't': 'ʇ',
                'u': 'n',
                'v': 'ʌ',
                'w': 'ʍ',
                'x': 'x',
                'y': 'ʎ',
                'z': 'z',
                '?': '¿',
                '.': '˙',
                ',': '\'',
                '(': ')',
                '<': '>',
                '[': ']',
                '{': '}',
                '\'': ',',
                '_': '‾'}

# append an inverted form of replacements to itself, so flipping works both ways
replacements.update(dict((v, k) for k, v in replacements.items()))

flippers = ["( ﾉ⊙︵⊙）ﾉ",
            "(╯°□°）╯",
            "( ﾉ♉︵♉ ）ﾉ",
            "(ﾉ ಠдಠ )ﾉ",
            "༼ノ◕ヮ◕༽ノ",
            "(╯=▃=)╯",
            "(ノ°▽°)ノ",
            "(╯ಠ‿ಠ)╯",
            "ʕ ⊃･ ◡ ･ ʔ⊃",
            "(╯ຈل͜ຈ) ╯",
            "(╯ ͝° ͜ʖ͡°)╯",
            "(つ☢益☢)つ",
            "(ﾉ＾◡＾)ﾉ"]
table_flipper = "┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻"


@listen_to(r'^.flip (.*)', re.IGNORECASE)
def flip(message, text):
    """
    <text> -- Flips <text> over.
    :param message: Slackbot message object
    :param text: Text to flip
    :return: Message to slack channel
    """
    global table_status
    chan = message._body['channel']

    if text in ['table', 'tables']:
        table_status[chan] = True
        return message.send(random.choice([random.choice(flippers) + " ︵ " + "┻━┻", table_flipper]))
    elif text == "5318008":
        out = "BOOBIES"
        return message.send(random.choice(flippers) + " ︵ " + out)
    elif text == "BOOBIES":
        out = "5318008"
        return message.send(random.choice(flippers) + " ︵ " + out)
    else:
        return message.send(random.choice(flippers) + " ︵ " + formatting.multi_replace(text[::-1], replacements))


@listen_to(r'^.table (.*)', re.IGNORECASE)
def table(message, text):
    """
    <text> -- (╯°□°）╯︵ <ʇxǝʇ>
    For lowercase flips
    :param message: Slackbot message object
    :param text: Text to flip
    :return: Message to slack channel
    """
    return message.send(random.choice(flippers) + " ︵ " + formatting.multi_replace(text[::-1].lower(), replacements))


@listen_to(r'^.fix (.*)', re.IGNORECASE)
def fix(message, text):
    """fixes a flipped over table. ┬─┬ノ(ಠ_ಠノ)"""
    global table_status
    chan = message._body['channel']

    if text in ['table', 'tables']:
        if table_status[chan]:
            table_status[chan] = False
            return message.send("┬─┬ノ(ಠ_ಠノ)")
        else:
            return message.send("no tables are currently turned over in this channel. Chill, yo.")
    else:
        return message.send(flip(message, text))
