#!/usr/bin/env python

import re
from stemming.porter2 import stem
import string
import urlparse

from lib.dbconfig import DatabaseDriver

# NLTK stop words collection
STOPWORDS = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves',
            'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under',
            'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during',
            'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where',
            'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out',
            'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we',
            'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against',
            's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her',
            'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until',
            'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he',
            'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my',
            'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have',
            'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other',
            'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i',
            'yours', 'so', 'the', 'having', 'once']
EMAILPAT = re.compile('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+')
FLOATPAT = re.compile(r'[+-]?\d+(:?\.\d*)?(:?[eE][+-]?\d+)?')
EXCLUDE = set(string.punctuation)


def remove_punctuations(text):
    text = ''.join(ch for ch in text if ch not in EXCLUDE)
    return text

def escape(word):
    if word in STOPWORDS or EMAILPAT.match(word) or FLOATPAT.match(word):
        return True

    urlseg = urlparse.urlparse(word)
    if urlseg.hostname and urlseg.scheme:
        return True

def filter(text):
    text = text.lower()
    words = text.split()
    tokens = [stem(word) for word in words if not escape(word)]
    text = ' '.join(token for token in tokens)
    text = remove_punctuations(text)
    return text

def sanitize():
    db = DatabaseDriver()
    db.setup()

    r = db.cur.execute('SELECT * FROM tweets')
    rows = r.fetchall()

    for row in rows:
        id, tweet, label = row
        ftweet = filter(tweet)
        print ftweet
        db.cur.execute('UPDATE tweets SET tweet=? WHERE id=?', (ftweet, id))
    db.conn.commit()
    db.teardown()

if __name__ == '__main__':
    #filter("#@$&(*!)*#Twitter surpasses 9.99 kailash.buki@gmail.com active monthly users: Twitter has not yet hit the saturation point. The ever-booming soci... http://t.co/DVeIMR1p")
    sanitize()
