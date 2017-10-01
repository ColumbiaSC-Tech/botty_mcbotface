# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import patch
from test_botty.mocks.mocks import MockMessage

# Import main functions
from botty_mcbotface.plugins.flipper import flip, fix

# Import data
from botty_mcbotface.plugins.flipper import flippers, table_flipper

# Short-circuit Message object that just returns results
mock_message = MockMessage()


class TestFlipper(TestCase):
    """
    Testing simple text flipping
    """
    def tearDown(self):
        del self

    def test_flip_requires_input(self):
        with self.assertRaises(TypeError):
            flip(mock_message)

    def test_flippers(self):
        res_flipper = flip(mock_message, 'flip_this').rsplit(' ︵ ')[0]
        self.assertTrue(res_flipper in flippers)

    def test_flipped_text(self):
        res_flipped = flip(mock_message, 'flip_this').rsplit(' ︵ ')[1]
        self.assertTrue(res_flipped == 'sᴉɥʇ‾dᴉןɟ')

    @patch('botty_mcbotface.plugins.flipper.sanitize_slack_str')
    def test_flip_slack_formatted_channel_name(self, mock_sanitize):
        mock_sanitize.return_value = '#testchannel'
        res_flipped = flip(mock_message, '<#C5G17UNEQ|testchannel>')

        self.assertTrue('ǝuuɐɥɔʇsǝʇ' in res_flipped)

    @patch('botty_mcbotface.plugins.flipper.sanitize_slack_str')
    def test_flip_slack_formatted_http_link(self, mock_sanitize):
        mock_sanitize.return_value = 'slack.com'
        res_flipped = flip(mock_message, '<http://slack.com|slack.com>')

        self.assertTrue('ɯoɔ˙ʞɔɐןs' in res_flipped)

    @patch('botty_mcbotface.plugins.flipper.sanitize_slack_str')
    def test_flip_slack_formatted_user_name(self, mock_sanitize):
        mock_sanitize.return_value = '@botty_mcbotface'
        res_flipped = flip(mock_message, '<@U5QPFMFP9>')

        self.assertTrue('ǝɔɐɟʇoqɔɯ‾ʎʇʇoq@' in res_flipped)


class TestTableFlipper(TestCase):
    """
    Testing `.flip table` and `.fix table(s)` together
    """
    def setUp(self):
        pass

    def tearDown(self):
        del self

    def test_fix_requires_input(self):
        with self.assertRaises(TypeError):
            fix(mock_message)

    def test_fixes_table(self):
        res_flipped = flip(mock_message, 'table')
        self.assertTrue('┻━┻' in res_flipped)

        res_fix = fix(mock_message, 'table')
        self.assertTrue('┬─┬ノ(ಠ_ಠノ)' in res_fix)

    def test_fixes_table_only_if_flipped(self):
        res_fix = fix(mock_message, 'table')
        self.assertTrue('No tables are currently turned over' in res_fix)
