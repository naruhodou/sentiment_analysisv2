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
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud 
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

# Plots two graphs together
def get_plot(f, g, s):
    x = sorted(f, key=f.__getitem__, reverse=True)
    y = []
    for i in x:
        y.append(f[i])
    n = min(len(x), 10)
    plt.subplot(2, 1, 1)
    plt.title('Positive ' + s)
    plt.barh(x[:n], y[:n])
    x = sorted(g, key=g.__getitem__, reverse=True)
    y = []
    for i in x:
        y.append(g[i])
    n = min(len(x), 10)
    plt.subplot(2, 1, 2)
    plt.barh(x[:n], y[:n])
    plt.title('Negitive ' + s)
    plt.show()

def sentiment_score(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    return score['compound']

class Tweet_Data:
    def __init__(self, file):
        self.file = file
        f = open(self.file, 'rt')
        data = csv.reader(f)
        self.date = []
        self.retweet_count = []
        self.text = []
        self.real_text = []
        self.hashtags = []
        self.pos_tweets = 0
        self.neg_tweets = 0
        self.no_of_tweets = 0
        for row in data:
            self.date.append(row[0])
            self.retweet_count.append(int(row[1]))
            self.text.append(row[2])
            self.real_text.append(row[2])
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
            temp = re.sub(r'[^\w\s]','', temp)
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

    def most_common_ngrams(self, n):
        ngram_count = {}
        for tweet in self.text:
            ngrams = nltk.ngrams(tweet.split(), n)
            for ngram in ngrams:
                if len(ngram) == 0:
                    continue
                if ngram not in ngram_count:
                    ngram_count[ngram] = 1
                else:
                    ngram_count[ngram] += 1
        ngram_counter = collections.Counter(ngram_count)
        num = 18 // n
        lst = ngram_counter.most_common(num)
        for i in range(num):
            s = ''
            for word in lst[i][0]:
                s += ' ' + word
            s = s[1:]
            lst[i] = (s, lst[i][1])
        plot_data(lst)
    
    def ngram_polarity(self, n):
        raw_data = ""
        for tweet in self.text:
            raw_data += tweet
        ngrams = nltk.ngrams(raw_data.split(), n)
        fdist = nltk.FreqDist(ngrams)
        pos = []
        neg = []
        sid = SentimentIntensityAnalyzer()    
        pos_bigrams=[]
        neg_bigrams=[]
        pf = {}
        nf = {}
        for key in fdist:
            ngram = ""
            for word in key:
                ngram += ' ' + word
            ngram = ngram[1:]
            if (sid.polarity_scores(ngram)['compound']) >= 0.5:
                if ngram not in pf:
                    pf[ngram] = 1
                else:
                    pf[ngram] += 1
            elif (sid.polarity_scores(ngram)['compound']) <= -0.5:
                if ngram not in nf:
                    nf[ngram] = 1
                else:
                    nf[ngram] += 1
        s = ""
        if n == 1:
            s = "Words"
        elif n == 2:
            s = "Bigrams"
        elif n == 3:
            s = "Trigrams"
        
        get_plot(pf, nf, s)
    
    def best_and_worst_tweet(self):
        best_score = -float('inf')
        best_tweet = ""
        for i in range(len(self.text)):
            score = sentiment_score(self.text[i])
            if score >= 0.5:
                self.pos_tweets += 1
            elif score <= -0.5:
                self.neg_tweets += 1
            if score > best_score:
                best_tweet, best_score = self.real_text[i][2:], score
        print("Best Review(score = {}): ".format(best_score), best_tweet)

        worst_score = float('inf')
        worst_tweet = ""
        for i in range(len(self.text)):
            score = sentiment_score(self.text[i])
            if score < worst_score:
                worst_tweet, worst_score = self.real_text[i][2:], score
        print("Worst Review(score = {}): ".format(worst_score), worst_tweet)
    
    def ngram_with_neg(self, n, s1):
        n += 1
        words = ""
        for tweet in self.text:
            words += tweet
        ng = nltk.ngrams(words.split(), n)
        f = {}
        sid = SentimentIntensityAnalyzer()
        for g in ng:
            s = ""
            for i in range(1, n):
                s += (g[i] + ' ')
            s = s[:len(s) - 1]
            if (sid.polarity_scores(g[0])['compound']) <= -0.5:
                if s not in f:
                    f[s] = 1
                else:
                    f[s] += 1
        x = sorted(f, key=f.__getitem__, reverse=True)
        y = []
        for i in x:
            y.append(f[i])
        n = min(len(x), 10)
        plt.title(s1 + ' preceded with negative words')
        plt.barh(x[:n], y[:n])
        plt.show()

    def word_cloud(self):
        comment_words = ' ' 
        for val in self.text: 
            tokens = val.split() 
            for i in range(len(tokens)): 
                tokens[i] = tokens[i].lower() 
            for words in tokens: 
                comment_words = comment_words + words + ' '
        wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white', 
                        min_font_size = 10).generate(comment_words)                     
        plt.figure(figsize = (8, 8), facecolor = None) 
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.tight_layout(pad = 0) 
        
        plt.show() 

tweets = Tweet_Data('tweets.csv')

####### Basic Stats #######

# print('Total Tweets: {}'.format(tweets.no_of_tweets))
# print('Tweets per week: {}'.format(tweets.tweet_per_week()))
# print('Tweets per month: {}'.format(tweets.tweet_per_month()))
# print('Tweets per year: {}'.format(tweets.tweet_per_year()))
# print('Average retweet count: {}'.format(tweets.get_avg_retweet_count()))

###########################

tweets.clean_tweets()
# tweets.ngram_polarity(1)
# tweets.best_and_worst_tweet()
# print("Number of positive tweets: ", tweets.pos_tweets)
# print("Number of negative tweets: ", tweets.neg_tweets)
# tweets.ngram_with_neg(2, 'Bigrams')
# tweets.ngram_with_neg(3, 'Trigrams')
tweets.word_cloud()