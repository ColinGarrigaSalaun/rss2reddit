import datetime
import unittest

from mock import call, patch, sentinel, Mock

import rss2reddit


class TestRss2(unittest.TestCase):

    @patch("feedparser.parse")
    @patch("praw.Reddit")
    def test(self, Reddit, parse):
        _entry_1 = Mock()
        _entry_2 = Mock()
        _entry_3 = Mock()
        _feed = parse.return_value
        _feed.entries = [
                _entry_1,
                _entry_2,
                _entry_3,
                ]
        
        rss2reddit.digest(
                reddit=sentinel.REDDIT,
                url=sentinel.URL,
                user=sentinel.USER,
                password=sentinel.PASSWORD)

        Reddit.assert_called_once_with("rss2reddit")
        _agent = Reddit.return_value
        self.assertEquals(_agent.submit.call_args_list,
            [
                call(sentinel.REDDIT, _entry_1.title, url=_entry_1.link),
                call(sentinel.REDDIT, _entry_2.title, url=_entry_2.link),
                call(sentinel.REDDIT, _entry_3.title, url=_entry_3.link),
                ])

    @patch("feedparser.parse")
    @patch("praw.Reddit")
    def test_since(self, Reddit, parse):
        _entry_1 = Mock()
        _entry_1.published = "Thu, 28 Jun 2001 14:17:15 +0000"
        _entry_2 = Mock()
        _entry_2.published = "Thu, 29 Jun 2001 14:17:15 +0000"
        _entry_3 = Mock()
        _entry_3.published = "Thu, 30 Jun 2001 14:17:15 +0000"
        _feed = parse.return_value
        _feed.entries = [
                _entry_1,
                _entry_2,
                _entry_3,
                ]
        
        rss2reddit.digest(
                reddit=sentinel.REDDIT,
                url=sentinel.URL,
                user=sentinel.USER,
                password=sentinel.PASSWORD,
                since=datetime.datetime(2001, 6, 29, 0, 0, 0))

        Reddit.assert_called_once_with("rss2reddit")
        _agent = Reddit.return_value
        self.assertEquals(_agent.submit.call_args_list,
            [
                call(sentinel.REDDIT, _entry_2.title, url=_entry_2.link),
                call(sentinel.REDDIT, _entry_3.title, url=_entry_3.link),
                ])

    @patch("feedparser.parse")
    @patch("praw.Reddit")
    def test_since__with_other_date_format(self, Reddit, parse):
        _entry_1 = Mock()
        _entry_1.published = "2001-06-28T14:17:15.000"
        _entry_2 = Mock()
        _entry_2.published = "2001-06-29T14:17:15.000"
        _entry_3 = Mock()
        _entry_3.published = "2001-06-30T14:17:15.000"
        _feed = parse.return_value
        _feed.entries = [
                _entry_1,
                _entry_2,
                _entry_3,
                ]
        
        rss2reddit.digest(
                reddit=sentinel.REDDIT,
                url=sentinel.URL,
                user=sentinel.USER,
                password=sentinel.PASSWORD,
                since=datetime.datetime(2001, 6, 29, 0, 0, 0))

        Reddit.assert_called_once_with("rss2reddit")
        _agent = Reddit.return_value
        self.assertEquals(_agent.submit.call_args_list,
            [
                call(sentinel.REDDIT, _entry_2.title, url=_entry_2.link),
                call(sentinel.REDDIT, _entry_3.title, url=_entry_3.link),
                ])

    @patch("feedparser.parse")
    @patch("praw.Reddit")
    def test_since__with_another_date_format(self, Reddit, parse):
        _entry_1 = Mock()
        _entry_1.date = "2001-06-28T14:17:15Z"
        _entry_1.published.side_effect = AttributeError()
        _entry_2 = Mock()
        _entry_2.date = "2001-06-29T14:17:15Z"
        _entry_2.published.side_effect = AttributeError()
        _entry_3 = Mock()
        _entry_3.date = "2001-06-30T14:17:15Z"
        _entry_3.published.side_effect = AttributeError()
        _feed = parse.return_value
        _feed.entries = [
                _entry_1,
                _entry_2,
                _entry_3,
                ]
        
        rss2reddit.digest(
                reddit=sentinel.REDDIT,
                url=sentinel.URL,
                user=sentinel.USER,
                password=sentinel.PASSWORD,
                since=datetime.datetime(2001, 6, 29, 0, 0, 0))

        Reddit.assert_called_once_with("rss2reddit")
        _agent = Reddit.return_value
        self.assertEquals(_agent.submit.call_args_list,
            [
                call(sentinel.REDDIT, _entry_2.title, url=_entry_2.link),
                call(sentinel.REDDIT, _entry_3.title, url=_entry_3.link),
                ])


