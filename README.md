# botty_mcbotface setup

## overview

A [slackbot](https://github.com/lins05/slackbot) plugin that acts as a general purpose Slack bot.
Although botty_mcbotface is not sentient, it does display a little sense of humor.

Much inspiration drawn from snoonet's [gonzobot](https://github.com/snoonetIRC/CloudBot) for IRC.
The main build is from lins05's [slackbot](https://github.com/lins05/slackbot), where botty_mcbotface
is essentially a plugin it as well as a sort of wrapper for with some extra
built-in features like a taskrunner, database (SQLite3). and a host of
pre-written plugins to start with.

## installation
*For more info on the setup for slackbot (number 2 & 3 below) you can read up [here](https://github.com/lins05/slackbot)*

1. Start a virtualenv in whatever directory you want to run botty,
    then cd into the project root and follow the remaining instructions

2. In your new project directory, create `slackbot_settings.py` from this template:
    ```
    API_TOKEN = 'your bot API token here'
    USER_TOKEN = 'your user API token here'

    # Default bot reply when pinged but has no command registered to respond with
    DEFAULT_REPLY = "Sorry but I didn't understand you"

    # User to send errors to in DM
    ERRORS_TO = 'danny'

    # Exclude list for .seen command channel/message search
    SEEN_PLUGIN_CHANNEL_BLACKLIST = ['admin']

    # If you want to set up the .calendar command you just need an ID.
    # You can also set up a cron job to check calendar at certain intervals for events and post.
    # To activate it set 'switch' to True and add apscheduler cron dict to 'schedule'.
    GOOGLE_CALENDAR = {
        'id': 'pk2pnrh8sj16dr6cquv37mc7sk@group.calendar.google.com',
        'cron': {
            'switch': True,
            'log_channel': 'C5G2L3F6H',  # Optionally send message to this channel when no events found
            'message_channel': 'C5G2L3F6H',  # Channel ID to message with event
            'schedule': {
                'second': '15'
                # 'hour': '9'
            }
        }
    }

    # Include all plugins like below, otherwise you can specify with multiple list items
    PLUGINS = [
        'botty_mcbotface.plugins'
    ]
    ```

3. Create a `run.py` file, this is the main entry point:
    ```
    #!/usr/bin/env python
    
    from slackbot.bot import Bot
    from botty_mcbotface import log
    from botty_mcbotface.task_runner import stop_task_runner


    def main():
        """Start slackbot"""
        
        try:
            bot = Bot()
            bot.run()
        except KeyboardInterrupt:
            log.info('Shutting down...')
            return stop_task_runner()


    if __name__ == "__main__":
        main()
    ```

4. Run `pip install botty-mcbotface`

5. Run `python run.py`:

6. To see the list of stock plugins and their commands, while botty is 
running in you Slack, type `.help` (make sure this is in a Slack channel 
that botty is also invited).

## contributors

[Danny Hinshaw](https://github.com/DannyHinshaw)

[Benjamin Matthews](https://github.com/bmatt468)

## license

The MIT License (see [LICENSE](LICENSE))
