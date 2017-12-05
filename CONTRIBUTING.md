# botty_mcbotface developer guide

Thanks for your interest in developing botty_mcbotface! These notes should help you produce pull
requests that will get merged without any issues.

As noted in the README, botty_mcbotface is an and implementation of
lins05's [slackbot](https://github.com/lins05/slackbot). This style guide is also a shameless pull
from the slackbot style-guide with some holes filled in. Mainly to keep consistency for any slackbot PR's,
as well as the similarities overall development, so credit to them there as well.

## Style guide

### Code style

There are places in the code that do not follow PEP 8 conventions. Do follow PEP 8 with new code,
but do not fix formatting throughout the file you're editing. If your commit has a lot of unrelated
reformatting in addition to your new/changed code, you may be asked to resubmit it with the extra changes removed.

### Commits

It's a good idea to use one branch per pull request. This will allow you to work on multiple changes at once.

Most pull requests should contain only a single commit. If you have to make corrections to a pull
request, rebase and squash your branch, then do a forced push. Clean up the commit message so it's
clear and as concise as needed.

## Development

These steps will help you prepare your development environment to work on botty_mcbotface.

### Setup

#### • Clone the repo

Begin by forking the repo. You will then clone your fork and add the central repo as another remote.
This will help you incorporate changes as you develop.

```
$ git clone git@github.com:yourusername/botty_mcbotface.git
$ cd botty_mcbotface
$ git remote add upstream git@github.com:lins05/botty_mcbotface.git
```

Do not make commits to develop, even in your local copy. All commits should be on a branch. Start your branch:

```
$ git checkout develop -b feature/name-of-feature
```

To incorporate upstream changes into your local copy and fork:

```
$ git checkout develop
$ git fetch upstream
$ git merge upstream/master
$ git push origin develop
```


See git documentation for info on merging, rebasing, and squashing commits.

#### • Setup Virtual Env (virtualenv/pyvenv)

A virtualenv allows you to install the Python packages you need to develop and run botty_mcbotface without
adding a bunch of unneeded junk to your system's Python installation. Once you create the virtualenv,
you need to activate it any time you're developing or running botty_mcbotface.
For Python 3, run:

```
$ pyvenv .env
```

Now that the virtualenv has been created, activate it and install the packages needed for development:

```
$ source .env/bin/activate
$ pip install -r requirements.txt
```

At this point, you should be able to run botty_mcbotface as described in the README.

### Testing

#### • Live Testing

In order to test botty_mcbotface live, you will need a slack instance. Create a free one at http://slack.com.
Do not use an existing Slack for tests, use a slack created just for development and test.

• Create a a new section in your `slackbot_settings.py`, "TESTING".

• Copy your original production settings, comment them out,
then paste and fill in your testing slack instance information.

Like so:
```
# ...your original/production settings here commented out

# TESTING

# Channels for .seen plugin to exclude in pulled message history
SEEN_PLUGIN_CHANNEL_BLACKLIST = ['admin']

# TESTING
API_TOKEN = 'xoxb-2368796695-uERgdhfsuihj31jih2UCz'
USER_TOKEN = 'xoxp-1853223687966-18679723582-2349123122586641-a4dc0fFHU329c8fc487cFS73JDKSf56180'
DEFAULT_REPLY = "Sorry but I didn't understand you"
ERRORS_TO = 'your_username'
PLUGINS = [
    'botty_mcbotface.plugins'
]
```

**Important note:** The bot token can be obtained by adding a custom bot
integration in Slack. User tokens can be obtained at
https://api.slack.com/docs/oauth-test-tokens. Slack tokens are like passwords!
Don't commit them. If you're using them in some kind of Github or Travis automation,
ensure they are for Slacks that are only for testing.

#### • Unit Testing

Please write unit tests for any new features or plugins you contribute. To run
the current unit tests use `nosetests`.

```
$ nosetests -v
```

Writing unit tests are fairly straightforward, botty also has some utilities
available in the `test_botty.mocks` module, the `MockMessage` and `MockRequestGET` classes.

Here's an example of their usage from the google plugin tests.

```
import os
import warnings
from nose.tools import assert_equals, assert_in, assert_true
from unittest import TestCase
from unittest.mock import patch
from test_botty.mocks import MockMessage, MockRequestGET
from botty_mcbotface.plugins.searches import google, youtube

# Short-circuit Message object that just returns results
mock_message = MockMessage()


class TestSearches(TestCase):
    def setUp(self):

        # lxml module throws warnings only relevant in production
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def tearDown(self):
        del self

    # Use of @patch('requests.get') in combination with MockRequestGET class
    # to mock a response message via data file in the test_botty.mocks directory
    @patch('requests.get')
    def test_google_search(self, mock_get_html):
        """Test google search retrieves first search result from google"""

        # Path to mock link results html file
        curr_dir = os.path.dirname(__file__)
        rel_path = '../../mocks/google_links.html'
        html_path = os.path.join(curr_dir, rel_path)

        mock_response = MockRequestGET(html_path)
        mock_get_html.return_value = mock_response

        # Call main method
        first_result = google(mock_message, 'testing')

        assert_equals('http://istqbexamcertification.com/what-is-software-testing/', first_result)

```

### Plugins

Finally, the fun stuff.
