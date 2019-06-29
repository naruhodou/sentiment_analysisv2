import tweepy
from tweepy import OAuthHandler
import csv
from auth_details import *
import math
import string
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
import re
import collections
import pandas as pd


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

def plot_data(lst):
    names, values = zip(*lst)
    ind = np.arange(len(lst))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, values, width, color='b')
    ax.set_ylabel('Count')
    ax.set_xticks(ind+width/2.)
    ax.set_xticklabels(names)
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    plt.show()

class Tweet_Data:
    def __init__(self, file):
        self.file = file
        f = open(self.file, 'rt')
        data = csv.reader(f)
        self.date = []
        self.retweet_count = []
        self.text = []
        self.hashtags = []
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
    
    def clean_tweets(self):
        stop_words = set(stopwords.words('english'))
        ps = PorterStemmer()
        
        for i in range(len(self.text)):
            temp = self.text[i][2:]
            temp = re.sub('x.*?6', '', temp)
            temp = temp.replace('\\', '')
            word_tokens = temp.split(' ')
            htags = []
            
            for word in word_tokens:
                if len(word) == 0:
                    continue
                if word[0] == '#':
                    htags.append(word[1:])
            self.hashtags.append(htags)

            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            temp = ""
            for word in filtered_sentence:
                if len(word) == 0:
                    continue
                cur_word = word
                if word[0] == '#':
                    cur_word = word[1:]
                temp += ' ' + ps.stem(cur_word)
            temp = temp[1:]
            temp = re.sub(r"(?:\@|https?\://)\S+", "", temp)
            self.text[i] = temp
    
    def most_common_words(self):
        word_count = {}
        for tweet in self.text:
            words = tweet.split(' ')
            for word in words:
                if len(word) == 0:
                    continue
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1
        word_counter = collections.Counter(word_count)
        lst = word_counter.most_common(10)
        plot_data(lst)

    def most_common_ngrams(n):
        pass

tweets = Tweet_Data('tweets.csv')

####### Basic Stats #######

# print('Total Tweets: {}'.format(tweets.no_of_tweets))
# print('Tweets per week: {}'.format(tweets.tweet_per_week()))
# print('Tweets per month: {}'.format(tweets.tweet_per_month()))
# print('Tweets per year: {}'.format(tweets.tweet_per_year()))
# print('Average retweet count: {}'.format(tweets.get_avg_retweet_count()))

###########################

tweets.clean_tweets()
tweets.most_common_words()