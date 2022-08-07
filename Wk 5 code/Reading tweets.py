#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on ???

@author: fitsstudiouser
"""

tweetData = 'http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/tweet_data.txt'

#fd = open('tweet_data.txt') # open local .txt file
import urllib

webFD = urllib.request.urlopen(tweetData)

ln = webFD.readline()

import json

tweet = json.loads(ln[6:])

tweet.keys()

tweet['created_at']
tweet['lang']
tweet['source']

tweetUser = tweet['user']

tweetUser['created_at']
tweet['user']['created_at']
tweet['created_at']

tweet['geo']
tweet['coordinates']








