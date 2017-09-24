# -*- coding: utf-8 -*-

import random
from collections import defaultdict

from slackbot.bot import listen_to, re

from botty_mcbotface.botty.api import sanitize_slack_str
from botty_mcbotface.utils import formatting
from botty_mcbotface.utils.tools import random_response

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
                'A': '∀',
                'B': 'ꓭ',
                'C': 'Ͻ',
                'D': 'ᗡ',
                'E': 'Ǝ',
                'F': 'ᖵ',
                'G': '⅁',
                'H': 'H',
                'I': 'I',
                'J': 'ᒋ',
                'K': 'ꓘ',
                'L': '⅂',
                'M': 'ꟽ',
                'N': 'N',
                'O': 'O',
                'P': 'Ԁ',
                'Q': 'Ꝺ',
                'R': 'ꓤ',
                'S': 'S',
                'T': 'ꓕ',
                'U': 'Ո',
                'V': 'Ʌ',
                'W': 'Ϻ',
                'X': 'X',
                'Y': '⅄',
                'Z': 'Z',
                '?': '¿',
                '.': '˙',
                ',': '\'',
                '(': ')',
                '<': '>',
                '^': 'v',
                '[': ']',
                '{': '}',
                '\'': ',',
                '_': '‾'}

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

fix_responses = ['Yea... I\'m not fixing that...',
                 '-___-',
                 'Staaaaaaahp',
                 'I CAN ONLY FIX TABLES OKAY?!',
                 'That\'s not a table!']

table_flipper = "┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻"

# Append an inverted form of replacements to itself, so flipping works both ways
replacements.update(dict((v, k) for k, v in replacements.items()))


@listen_to('^\.flip (.*)', re.IGNORECASE)
def flip(message, text):
    """
    <text> -- Flips <text> over.
    :param message: Slackbot message object
    :param text: Text to flip
    :return: Message to slack channel
    """
    global table_status
    chan = message._body['channel']
    re_table = re.compile('tables?$')

    if re.match(re_table, text.strip()):
        table_status[chan] = True
        return message.send(random_response([random.choice(flippers) + " ︵ " + "┻━┻", table_flipper]))
    elif text == "5318008":
        out = "BOOBIES"
        return message.send(random_response(flippers) + " ︵ " + out)
    elif text == "BOOBIES":
        out = "5318008"
        return message.send(random_response(flippers) + " ︵ " + out)
    else:
        # Clean up Slack formatted links, username's and channels.
        san_text = sanitize_slack_str(text)
        return message.send(random_response(flippers) + " ︵ " + formatting.multi_replace(san_text[::-1], replacements))


@listen_to('^\.fix (.*)', re.IGNORECASE)
def fix(message, text):
    """fixes a flipped over table. ┬─┬ノ(ಠ_ಠノ)"""
    global table_status
    chan = message._body['channel']

    if text in ['table', 'tables']:

        if table_status[chan]:
            table_status[chan] = False
            return message.send("┬─┬ノ(ಠ_ಠノ)")

        return message.send("No tables are currently turned over in this channel. Chill, yo.")

    # TODO: PR the slackbot repo for chaining methods (ie. return 'self')
    message.react('poop')
    return message.send(random_response(fix_responses))
