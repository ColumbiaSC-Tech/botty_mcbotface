from slackbot.bot import listen_to, re
from botty_mcbotface.utils.tools import random_response

responses = ['As I see it, yes',
             'It is certain',
             'It is decidedly so',
             'Most likely',
             'Outlook good',
             'Signs point to yes',
             'One would be wise to think so',
             'Naturally',
             'Without a doubt',
             'lol no',
             'Yes',
             'Yes, definitely',
             'You may rely on it',
             'Reply hazy, try again',
             'Ask again later',
             'Better not tell you now',
             'Cannot predict now',
             'Concentrate and ask again',
             'You know the answer better than I',
             'Maybe...',
             'You\'re kidding, right?',
             'Don\'t count on it',
             'In your dreams',
             'My reply is no',
             'My sources say no',
             'Outlook not so good',
             'Very doubtful']


@listen_to(r'^\.8ball |^\.8 |^\.eightball (.*)', re.IGNORECASE)
def eightball(message, _):
    """
    Ask the eightball a question and get a random response.
    :param message: Slackbot message object
    :param _:
    :return: Message to slack channel
    """
    return message.reply(random_response(responses))
