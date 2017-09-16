# -*- coding: utf-8 -*-

import random
from collections import defaultdict
from slackbot.bot import listen_to, re
from botty_mcbotface.utils import formatting
from botty_mcbotface.utils.api import get_user_name_by_id

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
        # When receiving text that is a tagged username, 'text' comes in as the ID(ie '@bot' == '<@43E6DG2>')
        # We switch out the id, check the slack API for the username associated with it and return that instead

        # Regex pattern to detect name-tags/user-ids
        re_user = re.compile('<@[A-Z0-9]*>')

        if re.search(re_user, text):
            matches = re.findall(re_user, text)

            for match in matches:
                # Extract the id from surrounding chars
                start, second = match.split('<@')
                user_id, end = second.split('>')

                # Query the Slack API
                # Piece it all back together
                user_name = '@' + get_user_name_by_id(user_id)
                text = re.sub(match, user_name, text)

            return message.send(random.choice(flippers) + " ︵ " + formatting.multi_replace(text[::-1], replacements))

        return message.send(random.choice(flippers) + " ︵ " + formatting.multi_replace(text[::-1], replacements))


@listen_to('^\.fix (.*)', re.IGNORECASE)
def fix(message, text):
    """fixes a flipped over table. ┬─┬ノ(ಠ_ಠノ)"""
    global table_status
    chan = message._body['channel']

    if text in ['table', 'tables']:

        if table_status[chan]:
            table_status[chan] = False
            return message.send("┬─┬ノ(ಠ_ಠノ)")

        return message.send("no tables are currently turned over in this channel. Chill, yo.")

    return message.send(flip(message, text))
