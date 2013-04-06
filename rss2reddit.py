#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import logging

import feedparser
import praw

logging.basicConfig(
        filename="rss2reddit.log",
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s')


def digest(reddit="", url="", user="", password="", since=None):
    logging.info((reddit, url, user, password, since))
    _agent = praw.Reddit("rss2reddit")
    _agent.login(user, password)

    _stream = feedparser.parse(url)

    for _post in _stream.entries:
        if since:
            try:
                _published = datetime.datetime.strptime(_post.published[:-6], "%a, %d %b %Y %H:%M:%S")
            except ValueError:
                _example = "2001-06-30T14:17:15"
                _published = datetime.datetime.strptime(_post.published[:len(_example)], "%Y-%m-%dT%H:%M:%S")
            if _published >= since:
                logging.info("Submitting %s (%s)", _post.title, _post.link)
                _agent.submit(reddit, _post.title, url=_post.link)
        else:
            logging.info("Submitting %s (%s)", _post.title, _post.link)
            _agent.submit(reddit, _post.title, url=_post.link)


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
            "reddit": _args.reddit,
            "user": _args.user,
            "password": _args.password,
            }
    if _args.days:
        _kwargs["since"] = datetime.datetime.today() - datetime.timedelta(days=_args.days)


    _filename = _args.url_file
    if _filename:
        with open(_filename) as _file:
            for _line in _file:
                _kwargs["url"] = _line[:-1]
                try:
                    digest(**_kwargs)
                except BaseException, ex:
                    logging.error(ex)
    else:
        _kwargs["url"] = _args.url
        try:
            digest(**_kwargs)
        except BaseException, ex:
            logging.error(ex)

