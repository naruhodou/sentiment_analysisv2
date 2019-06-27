import tweepy
from tweepy import OAuthHandler
import csv
from auth_details import *
import math
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

####### Reads Tweets Into tweets.csv File #######

# csvFile = open('tweets.csv', 'a')
# csvWriter = csv.writer(csvFile)
# hashtags = ['#trek', '#treksinindia', '#trekfanatics', '#trekmaniac', '#trekmunk']
# tweets = []
# for hashtag in hashtags:
#     fetch_tweets = tweepy.Cursor(api.search,
#                 q=hashtag,
#                 lang="en").items()
#     for tweet in fetch_tweets:
#         tweets.append(tweet._json)
#         csvWriter.writerow([tweet.created_at, tweet._json['retweet_count'], tweet.text.encode('utf-8')])

# csvFile.close()

###################################################


###################################################

# csv format: Date|Number of Retweets|Text

###################################################
class Tweet_Data:
    def __init__(self, file):
        self.file = file
        f = open(self.file, 'rt')
        data = csv.reader(f)
        self.date = []
        self.retweet_count = []
        self.text = []
        self.no_of_tweets = 0
        for row in data:
            self.date.append(row[0])
            self.retweet_count.append(int(row[1]))
            self.text.append(row[2])
            self.no_of_tweets += 1
        f.close()
    def get_weeks(self):
        d1 = datetime.strptime(self.date[0], '%Y-%m-%d %H:%M:%S')
        d0 = datetime.strptime(self.date[self.no_of_tweets - 1], '%Y-%m-%d %H:%M:%S')
        delta = d1 - d0
        ans = (delta.days / 7)
        return ans

    def get_years(self):
        d1 = datetime.strptime(self.date[0], '%Y-%m-%d %H:%M:%S')
        d0 = datetime.strptime(self.date[self.no_of_tweets - 1], '%Y-%m-%d %H:%M:%S')
        delta = d1 - d0
        ans = (delta.days / 365)
        return ans
    
    def tweet_per_week(self):
        return (self.no_of_tweets / self.get_weeks())

    def tweet_per_year(self):
        return (self.no_of_tweets / self.get_years())

    def tweet_per_month(self):
        return (self.tweet_per_year() / 12)

    def get_avg_retweet_count(self):
        ans = 0
        for i in self.retweet_count:
            ans += i
        ans /= self.no_of_tweets
        return ans

tweets = Tweet_Data('tweets.csv')
print('Total Tweets: {}'.format(tweets.no_of_tweets))
print('Tweets per week: {}'.format(tweets.tweet_per_week()))
print('Tweets per month: {}'.format(tweets.tweet_per_month()))
print('Tweets per year: {}'.format(tweets.tweet_per_year()))
print('Average retweet count: {}'.format(tweets.get_avg_retweet_count()))
