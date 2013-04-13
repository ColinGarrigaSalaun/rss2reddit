#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import logging

import feedparser
import praw

USER_AGENT = "rss2reddit"


logging.basicConfig(
        filename="rss2reddit.log",
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s')


def digest(reddit="", user="", password="", url="", since=None, file_url=""):
    _posts = [
            _post
            for _url in _urls(url, file_url)
            for _post in _entries(_url)
            if not since or _date(_post) >= since]
    
    if _posts:
        _agent = praw.Reddit(USER_AGENT)
        _agent.login(user, password)
        for _post in _posts:
            logging.info("Submitting %s (%s)", _post.title, _post.link)
            _agent.submit(reddit, _post.title, url=_post.link)


def _entries(url):
    logging.info("Reading %s" % url)
    return feedparser.parse(url).entries


def _urls(url, file_url):
    try:
        with open(file_url) as _file:
            return [_line[:-1] for _line in _file]
    except IOError:
        return [url]


def _date(post):
    for _example, _format, _attribute in (
            ("Thu, 28 Jun 2001 14:17:15", "%a, %d %b %Y %H:%M:%S", "published"),
            ("2001-06-28T14:17:15",       "%Y-%m-%dT%H:%M:%S",     "published"),
            ("2001-06-28T14:17:15",       "%Y-%m-%dT%H:%M:%S",     "date")):
        try:
            _date = getattr(post, _attribute)
            _parsable_date = _date[:len(_example)]
            return datetime.datetime.strptime(_parsable_date, _format)
        except BaseException:
            pass


if __name__ == "__main__":
    _parser = argparse.ArgumentParser("Post rss items on Reddit")
    _parser.add_argument('--reddit',   required=True, help="subreddit's name to post to")
    _parser.add_argument('--user',     required=True, help='Reddit user')
    _parser.add_argument('--password', required=True, help="Reddit user's password")
    _parser.add_argument('--url',                     help='feed URL')
    _parser.add_argument('--url-file',                help='file containing feeds URL')
    _parser.add_argument('--days',                    help='number of days to look back', type=int)

    _args = _parser.parse_args()
    _kwargs = {
            "reddit":   _args.reddit,
            "user":     _args.user,
            "password": _args.password,
            "url":      _args.url,
            "since":    _args.days and datetime.datetime.today() - datetime.timedelta(days=_args.days) or None,
            "file_url": _args.url_file,
            }
    logging.info(_kwargs)
    try:
        digest(**_kwargs)
    except BaseException, ex:
        logging.error(ex)

