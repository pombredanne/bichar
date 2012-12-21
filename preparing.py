#!/usr/bin/env python

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
        """
        self.dbd.cur.execute("SELECT tweet FROM tweets WHERE tweet=?", (tweet,))
        already_in_db = self.dbd.cur.fetchone()
        if not already_in_db:
            self.dbd.cur.execute("INSERT INTO tweets(tweet) VALUES(?)", (tweet,))
        print 'duplicate!!!'

    def mine(self, query, rpp, max_tweets):
        """prepares test data for training
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

