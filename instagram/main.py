    # This script is written for personal research and is not endorsed by Instagram.
# Use at your own risk!
# -*- coding: utf-8 -*-
import csv
import requests
import urllib.request
import json
import re
import random
import time
from fake_useragent import UserAgent
from random import randint
from time import sleep

ua = UserAgent(cache=False)
ts = time.gmtime()
timestamp = time.strftime("%d-%m-%Y %H-%M", ts)

def get_csv_header(top_numb):
        fieldnames = ['Hashtag','Active Days Ago','Post Count','AVG. Likes','MAX. Likes','MIN. Likes','AVG. Comments','Hashtag URL','Post Ready Tag']
        return fieldnames

def write_csv_header(filename, headers):
        with open(filename, 'w', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=headers)
            writer.writeheader()
        return

def read_keywords(t_file):
        with open(t_file) as f:
            keyword_list = f.read().splitlines()
        return keyword_list

def read_proxies(p_file):
        with open(p_file) as f:
            proxy_list = f.read().splitlines()
        return proxy_list

#file 
data_filename = 'Hashtag Scrape ' + timestamp + '.csv'
KEYWORD_FILE = './hashtags.txt'
DATA_FILE = './' + data_filename
PROXY_FILE = './proxies.txt'
keywords = read_keywords(KEYWORD_FILE)
proxies = read_proxies(PROXY_FILE)
csv_headers = get_csv_header(9)
write_csv_header(DATA_FILE, csv_headers)

#Ask for randomisation input fields
low = input("Please enter minimal delay time (in seconds): ")
low_random = int(low)
high = input("Please enter maximal delay time (in seconds): ")
high_random = int(high)

#get the data
for keyword in keywords:
    import urllib, json
    if len(proxies)!=0:
        proxy_ip = random.choice(proxies)
        proxy_support = urllib.request.ProxyHandler({'https':proxy_ip})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
    prepare_url = urllib.request.Request(
        'https://www.instagram.com/explore/tags/' + urllib.parse.quote_plus(keyword) + '/?__a=1',
        headers={
            'User-Agent': ua.random
        }
    )
    url = urllib.request.urlopen(prepare_url)
    post_info = {}
    response = json.load(url) #response is the JSON dump of the url.

    #defining some script helpers
    x = len(response['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'])
    i = avg_post_likes = 0
    likes_value = []
    comments_value = []

    #Getting the general tag data
    hashtag_name = response['graphql']['hashtag']['name']
    post_count = response['graphql']['hashtag']['edge_hashtag_to_media']['count']
    hashtag_url = 'https://www.instagram.com/explore/tags/' + keyword
    post_ready_tag = '#' + keyword 
    top_posts = response['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']

    #calculate the active days ago 
    most_recent_post = response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][0]['node']['taken_at_timestamp']
    import datetime
    from dateutil import relativedelta
    post_datetime = datetime.datetime.fromtimestamp(most_recent_post).strftime('%Y-%m-%d %H:%M:%S')
    post_cleandate = datetime.datetime.fromtimestamp(most_recent_post).strftime('%Y-%m-%d')
    from datetime import datetime, date
    most_recent_clean = datetime.strptime(post_cleandate, '%Y-%m-%d')
    today = datetime.strptime(str(date.today()),'%Y-%m-%d')
    posted_days_ago = relativedelta.relativedelta(today, most_recent_clean).days

    while i <=x-1:
        #Getting data from top posts
        top_post_likes = response['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'][i]['node']['edge_liked_by']
        post_like = response['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'][i]['node']['edge_liked_by']['count']
        post_comment = response['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'][i]['node']['edge_media_to_comment']['count']
        likes_value.append(post_like)
        comments_value.append(post_comment)
        i += 1
    print('Writing ' + keyword + ' to output file')
    with open(data_filename, 'a', newline='',  encoding='utf-8') as data_out:
            post_info["Hashtag"] = hashtag_name
            post_info["Active Days Ago"] = posted_days_ago
            post_info["Post Count"] = post_count
            post_info["AVG. Likes"] = round(sum(likes_value)/len(likes_value),2)
            post_info["MAX. Likes"] = max(likes_value)
            post_info["MIN. Likes"] = min(likes_value)
            post_info["AVG. Comments"] = round(sum(comments_value)/len(comments_value),2)
            post_info["Hashtag URL"] = hashtag_url
            post_info["Post Ready Tag"] = post_ready_tag
            csv_writer = csv.DictWriter(data_out, fieldnames=csv_headers)
            csv_writer.writerow(post_info)

    #Randomly pause script based on input values
    sleep(randint(low_random,high_random))
#cleaning up the file: 
destination = data_filename[:-4] + '_unique.csv'
data = open(data_filename, 'r',encoding='utf-8')
target = open(destination, 'w',encoding='utf-8')
# Let the user know you are starting, in case you are de-dupping a huge file 
print("\nRemoving duplicates from %r" % data_filename)

# Initialize variables and counters
unique_lines = set()
source_lines = 0
duplicate_lines = 0

# Loop through data, write uniques to output file, skip duplicates.
for line in data:
    source_lines += 1
    # Strip out the junk for an easy set check, also saves memory
    line_to_check = line.strip('\r\n')  
    if line_to_check in unique_lines: # Skip if line is already in set
        duplicate_lines += 1
        continue 
    else: # Write if new and append stripped line to list of seen lines
        target.write(line)
        unique_lines.add(line_to_check)
# Be nice and close out the files
target.close()
data.close()
import os
os.remove(data_filename)
os.rename(destination, data_filename)
print("SUCCESS: Removed %d duplicate line(s) from file with %d line(s)." % \
 (duplicate_lines, source_lines))
print("Wrote output to %r\n" % data_filename)
print("\n" + 'ALL DONE !!!! ')