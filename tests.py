import datetime
import unittest

from mock import call, patch, sentinel, Mock

import rss2reddit


class TestRss2(unittest.TestCase):

    @patch("feedparser.parse")
    @patch("praw.Reddit")
    def test(self, Reddit, parse):
        _feed = parse.return_value
        _feed.entries = [_entry_1, _entry_2, _entry_3] = [Mock(), Mock(), Mock()]
        
        rss2reddit.digest(
                reddit=sentinel.REDDIT,
                url=sentinel.URL,
                user=sentinel.USER,
                password=sentinel.PASSWORD)

        Reddit.assert_called_once_with(rss2reddit.USER_AGENT)
        _agent = Reddit.return_value
        self.assertEquals(_agent.submit.call_args_list,
            [
                call(sentinel.REDDIT, _entry_1.title, url=_entry_1.link),
                call(sentinel.REDDIT, _entry_2.title, url=_entry_2.link),
                call(sentinel.REDDIT, _entry_3.title, url=_entry_3.link),
                ])


    @patch("feedparser.parse")
    @patch("praw.Reddit")
    @patch("rss2reddit._date")
    def test_since(self, _date, Reddit, parse):
        _feed = parse.return_value
        _feed.entries = [_entry_1, _entry_2, _entry_3] = [Mock(), Mock(), Mock()]
        _date.side_effect = lambda p: {
                _entry_1: datetime.datetime(2001, 6, 28, 14, 17, 15),
                _entry_2: datetime.datetime(2001, 6, 29, 14, 17, 15),
                _entry_3: datetime.datetime(2001, 6, 30, 14, 17, 15),
                }[p]
        
        rss2reddit.digest(
                reddit=sentinel.REDDIT,
                url=sentinel.URL,
                user=sentinel.USER,
                password=sentinel.PASSWORD,
                since=datetime.datetime(2001, 6, 29, 0, 0, 0))

        _agent = Reddit.return_value
        Reddit.assert_called_once_with(rss2reddit.USER_AGENT)
        self.assertEquals(_agent.submit.call_args_list,
            [
                call(sentinel.REDDIT, _entry_2.title, url=_entry_2.link),
                call(sentinel.REDDIT, _entry_3.title, url=_entry_3.link),
                ])


    @patch("feedparser.parse")
    @patch("praw.Reddit")
    @patch("rss2reddit._date")
    def test_since__and_empty(self, _date, Reddit, parse):
        _feed = parse.return_value
        _feed.entries = [_entry_1, _entry_2, _entry_3] = [Mock(), Mock(), Mock()]
        _date.side_effect = lambda p: {
                _entry_1: datetime.datetime(2001, 6, 28, 14, 17, 15),
                _entry_2: datetime.datetime(2001, 6, 29, 14, 17, 15),
                _entry_3: datetime.datetime(2001, 6, 30, 14, 17, 15),
                }[p]
        
        rss2reddit.digest(
                reddit=sentinel.REDDIT,
                url=sentinel.URL,
                user=sentinel.USER,
                password=sentinel.PASSWORD,
                since=datetime.datetime(2001, 7, 1, 0, 0, 0))

        self.assertFalse(Reddit.called)


    @patch("__builtin__.open")
    @patch("feedparser.parse")
    @patch("praw.Reddit")
    def test_with_file(self, Reddit, parse, _open):
        _feed_1 = Mock()
        _feed_1.entries = [_entry_1, _entry_2] = [Mock(), Mock()]
        _feed_2 = Mock()
        _feed_2.entries = [_entry_3, _entry_4] = [Mock(), Mock()]
        _file = _open.return_value.__enter__.return_value
        _file.__iter__.return_value = ["url_1\n", "url_2\n"]
        parse.side_effect = lambda url: {
                "url_1": _feed_1,
                "url_2": _feed_2,
                }.get(url)
        
        rss2reddit.digest(
                reddit=sentinel.REDDIT,
                user=sentinel.USER,
                password=sentinel.PASSWORD,
                file_url=sentinel.FILENAME)

        Reddit.assert_called_once_with(rss2reddit.USER_AGENT)
        _agent = Reddit.return_value
        self.assertEquals(_agent.submit.call_args_list,
            [
                call(sentinel.REDDIT, _entry_1.title, url=_entry_1.link),
                call(sentinel.REDDIT, _entry_2.title, url=_entry_2.link),
                call(sentinel.REDDIT, _entry_3.title, url=_entry_3.link),
                call(sentinel.REDDIT, _entry_4.title, url=_entry_4.link),
                ])



class TestDate(unittest.TestCase):

    def test(self):
        for _example, _attribute in (
                ("Thu, 28 Jun 2001 14:17:15 +0000", "published"),
                ("2001-06-28T14:17:15.000",         "published"),
                ("2001-06-28T14:17:15Z",            "date"),):
            _entry = Mock()
            _entry.published.side_effect = AttributeError()
            _entry.date.side_effect = AttributeError()
            setattr(_entry, _attribute, _example)

            _datetime = rss2reddit._date(_entry)

            self.assertEquals(datetime.datetime(2001, 6, 28, 14, 17, 15), _datetime)
            
