.. raw:: html

   <!--For conversion to rst run the command below from project root-->

.. raw:: html

   <!--pandoc --from=markdown --to=rst README.md -o README.rst-->

Setup
=====

Overview
--------

A `slackbot <https://github.com/lins05/slackbot>`__ plugin that acts as
a general purpose Slack bot. Although botty\_mcbotface is not sentient,
it does display a little sense of humor.

Much inspiration drawn from snoonet's
`gonzobot <https://github.com/snoonetIRC/CloudBot>`__ for IRC. The main
build is from lins05's
`slackbot <https://github.com/lins05/slackbot>`__, which
botty\_mcbotface is technically a plugin for (though he himself has a
multitude of plugins as well).

Installation
------------

*For more info on the setup for slackbot (number 2 & 3 below) you can
read up `here <https://github.com/lins05/slackbot>`__*

1. Start a virtualenv in whatever directory you want to run botty, then
   cd into it and follow the instructions

2. In your new project directory, create a ``slackbot_settings.py``:

   ::

       API_TOKEN = 'your bot API token here'

       # Default bot reply when pinged but has no command registered to respond with
       DEFAULT_REPLY = "Sorry but I didn't understand you"

       # User to send errors to in DM
       ERRORS_TO = 'danny'

       # Include all plugins like below, otherwise you can specify with multiple list items
       PLUGINS = [
           'botty_mcbotface.plugins'
       ]

3. Create a ``run.py`` file, this is the main entry point:

   ::

       #!/usr/bin/env python
       from slackbot.bot import Bot
       import logging
       logging.basicConfig()


       def main():
           bot = Bot()
           bot.run()

       if __name__ == "__main__":
           main()

4. Run ``pip install botty_mcbotface``

5. Run ``python run.py``:

Contributors
------------

`Danny Hinshaw <https://github.com/DannyHinshaw>`__

License
-------

The MIT License (see `LICENSE <LICENSE>`__)
