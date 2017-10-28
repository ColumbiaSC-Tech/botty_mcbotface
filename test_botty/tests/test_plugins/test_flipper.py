# -*- coding: utf-8 -*-
from nose.tools import assert_in, assert_true, assert_raises
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
        """Test flipper raises TypeError when no input given"""
        with assert_raises(TypeError):
            flip(mock_message)

    def test_flippers(self):
        """Test flipper responses are valid"""
        res_flipper = flip(mock_message, 'flip_this').rsplit(' ︵ ')[0]
        assert_in(res_flipper, flippers)

    def test_flipped_text(self):
        """Test flipper flips text upside down"""
        res_flipped = flip(mock_message, 'flip_this').rsplit(' ︵ ')[1]
        assert_true(res_flipped == 'sᴉɥʇ‾dᴉןɟ')

    @patch('botty_mcbotface.plugins.flipper.sanitize_slack_str')
    def test_flip_slack_formatted_channel_name(self, mock_sanitize):
        """Test flipper outputs reformatted slack channel names"""
        mock_sanitize.return_value = '#testchannel'
        res_flipped = flip(mock_message, '<#C5G17UNEQ|testchannel>')

        assert_in('ǝuuɐɥɔʇsǝʇ', res_flipped)

    @patch('botty_mcbotface.plugins.flipper.sanitize_slack_str')
    def test_flip_slack_formatted_http_link(self, mock_sanitize):
        """Test flipper outputs reformatted slack http links"""
        mock_sanitize.return_value = 'slack.com'
        res_flipped = flip(mock_message, '<http://slack.com|slack.com>')

        assert_in('ɯoɔ˙ʞɔɐןs', res_flipped)

    @patch('botty_mcbotface.plugins.flipper.sanitize_slack_str')
    def test_flip_slack_formatted_user_name(self, mock_sanitize):
        """Test flipper outputs reformatted slack user names"""
        mock_sanitize.return_value = '@botty_mcbotface'
        res_flipped = flip(mock_message, '<@U5QPFMFP9>')

        assert_in('ǝɔɐɟʇoqɔɯ‾ʎʇʇoq@', res_flipped)


class TestTableFlipper(TestCase):
    """
    Testing `.flip table` and `.fix table(s)` together
    """
    def setUp(self):
        pass

    def tearDown(self):
        del self

    def test_fix_requires_input(self):
        """Test table fixer requires user input"""
        with assert_raises(TypeError):
            fix(mock_message)

    def test_fixes_table(self):
        """Test table fixer can fix flipped tables"""
        res_flipped = flip(mock_message, 'table')
        assert_in('┻━┻', res_flipped)

        res_fix = fix(mock_message, 'table')
        assert_in('┬─┬ノ(ಠ_ಠノ)', res_fix)

    def test_fixes_table_only_if_flipped(self):
        """Test table fixer detects when no tables have been flipped"""
        res_fix = fix(mock_message, 'table')
        assert_in('No tables are currently turned over', res_fix)
