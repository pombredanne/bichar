bichar
======

Twitter Sentiment Analyzer based on Naive Baysian Classifier


Setting up
==========

1. `python preparing.py` => crawls twitter search data & saves into the db
2. `cd web && python app.py` => runs the server which allows for refining and labelling from browser
3. `python clearing.py` => filters noise and unwanted words from tweets
4. `python training.py` => to test the test set accuracy OR import this module to predict labels for new tweets


Dependencies
============

- python-flask
- stemming
- python-requests

