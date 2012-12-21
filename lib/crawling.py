#!/usr/bin/env python


import json
import requests
from urllib import quote

from configreading import ConfigReader as cfgreader


class Crawler(object):
    """
    """
    def __init__(self, query, rpp, max_tweets):
        """
        """
        self.query = query
        self.seed_url = 'http://search.twitter.com/search.json'
        self.rpp = rpp
        self.max_tweets = max_tweets
        self.tweets = []

    def start(self, next_page=None):
        """
        """
        if next_page:
            search_url = '%s%s&lang=en' % (self.seed_url, next_page)
        else:
            search_url = '%s?q=%s&rpp=%s&lang=en' % (self.seed_url, quote(self.query), self.rpp)
        print 'tweet_count=%s url=%s' % (len(self.tweets), search_url)
        response = requests.get(search_url)
        search_result = json.loads(response.content)
        tweets = search_result['results']

        for tweet in tweets:
            if tweet['text'].startswith('RT'):
                continue
            if len(self.tweets) == self.max_tweets:
                return
            last_id = tweet['id']
            self.tweets.append(u'%s'  % tweet['text'].strip())

        if search_result.has_key('next_page'):
            next_page = '?max_id=%s&rpp=%s&q=%s' % (last_id, self.rpp,
                                                    quote(search_result['query']))
            self.start(next_page=next_page)


if __name__ == '__main__':
    crawler = Crawler('obama', 100, 5000)
    crawler.start()
