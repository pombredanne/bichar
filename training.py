#!/usr/bin/env python
# Author: kailash.buki@gmail.com
# Use this script to test the test set accuracy, predict the label for new tweets

from operator import mul, itemgetter

from lib.dbconfig import DatabaseDriver
from clearing import filter

TRAINING_SET = 300 # total rows to be used for training set, this can be changed


def get_all_tweets():
    """returns all the tweets in db

    Returns:
        rows: list of tuples. For example;
                [('this is a test positive tweet', 'pos'),
                ('this is a test negative tweet', 'neg'), ...]
    """
    db = DatabaseDriver()
    db.setup()
    r = db.cur.execute('SELECT tweet, label FROM tweets')
    rows = r.fetchall()
    db.teardown()
    return rows

def get_feature_vector(rows):
    """returns the feature vector

    Args:
        rows: list of tuples. For example;
                [
                    ('this is a test positive tweet', 'pos'),
                    ('this is a test negative tweet', 'neg'),
                    ...
                ]

    Returns:
        vec: nested dictionary, which contains the labels and under each labels contains
                another dict where keys are the tokens and values are their frequency in
                that label. For example;
                {
                    'pos': {'love': 5, 'like': 3, ...},
                    'neg': {'hate': 4, 'dont': 3, 'like': 1, ...},
                    ...
                }
    """
    vec = dict()
    for row in rows:
        tweet, label = row
        toks = tweet.split()

        if not vec.has_key(label):
            vec[label] = dict()

        for tok in toks:
            if vec[label].has_key(tok):
                vec[label][tok] += 1
            else:
                vec[label][tok] = 1
    return vec

def predict(tweet):
    """predicts the label by using naive baysian classifier

    Args:
        tweet: text string

    Returns:
        label: string representing the predicted label
    """
    tweet = filter(tweet)
    rows = get_all_tweets()
    vec = get_feature_vector(rows[:TRAINING_SET])

    label_count = dict()
    for label in vec.keys():
        label_count[label] = sum(vec[label].values())

    def prior_prob(label):
        """calculates the prior probability
        """
        num_label = label_count[label]
        total_labels = sum(label_count.values())
        return  num_label * 1.0 / total_labels

    def likelihood_prob(tok, label):
        """calculates the likelihood
        """
        try:
            num_tok_label = vec[label][tok]
        except KeyError:
            num_tok_label = 0
        num_labels = label_count[label]
        return num_tok_label * 1.0 / num_labels

    posterior_prob = dict()
    toks = tweet.split()
    for label in vec.keys():
        prior = prior_prob(label)
        likelihoods = []
        for tok in toks:
            likelihoods.append(likelihood_prob(tok, label))
        likelihood_prod = reduce(mul, likelihoods)
        posterior_prob[label] = prior * likelihood_prod
    sorted_posterior_prob = sorted(posterior_prob.iteritems(), key=itemgetter(1), reverse=True)
    predicted_label = sorted_posterior_prob[0][0]
    return predicted_label

def test():
    """Runs the model against the test set to calculate the accuracy of the model
    """
    rows = get_all_tweets()[:TRAINING_SET] # test set
    total = len(rows)
    correct = 0
    for row in rows:
        tweet, label = row
        predicted_label = predict(tweet)
        if label == predicted_label:
            correct += 1

    print 'TEST ACCURACY=%s' % (correct * 100.0 / total)


if __name__ == '__main__':
    test()
    print predict("i don't like others telling me what to do in twitter")
