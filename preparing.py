#!/usr/bin/env python
# Author: kailash.buki@gmail.com
# Run this script to crawl tweets and save them in db

from lib.crawling import Crawler
from lib.dbconfig import DatabaseDriver


class Miner(object):
    """
    """
    def __init__(self):
        self.dbd = DatabaseDriver()
        self.dbd.setup()
        self.dbd.ensure_table()

    def save(self, tweet):
        """saves tweet to the db

        Args:
            tweet: text string
        """
        self.dbd.cur.execute("SELECT tweet FROM tweets WHERE tweet=?", (tweet,))
        already_in_db = self.dbd.cur.fetchone()
        if not already_in_db:
            self.dbd.cur.execute("INSERT INTO tweets(tweet) VALUES(?)", (tweet,))
        print 'duplicate!!!'

    def mine(self, query, rpp, max_tweets):
        """prepares test data for training

        Args:
            query: search query to be used in twitter search
            rpp: rate per page is the param to the twitter search url
            max_tweets: maximum number of tweets to crawl
        """
        crawler = Crawler(query, rpp, max_tweets)
        crawler.start()

        tweets = crawler.tweets
        for tweet in tweets:
            self.save(tweet)

        self.dbd.conn.commit()
        self.dbd.teardown()


if __name__ == '__main__':
    worker = Miner()
    worker.mine('twitter', 100, 900)

