#WORKING

import tweepy
import configparser
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

config = configparser.ConfigParser()

config.read('config.ini')

CONSUMER_KEY = config['twitter']['consumer_key']
CONSUMER_SECRET = config['twitter']['CONSUMER_SECRET']
ACCESS_TOKEN = config['twitter']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = config['twitter']['ACCESS_TOKEN_SECRET']
BEARER_TOKEN = config['twitter']['BEARER_TOKEN']
API_KEY =config['twitter']['api_key'] 
API_KEY_SECRET =config['twitter']['api_key_secret']

# Authenticate to Twitter

client = tweepy.Client(bearer_token=BEARER_TOKEN,consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

#auth = tweepy.OAuthHandler(CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
#uth.set_access_token(access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

def get_timeline(expansions):
    return client.get_home_timeline(max_results=10, user_auth=True, expansions = expansions)

def is_duplicate(stream):
    if type(stream) != 'list':
        return("Error. Passed parameter is Not a list")
    if len(stream) != len(set(stream)):
        return True
    else:
        return False

def is_match(stream):
    if type(stream) != 'dict':
        return("Error. Passed parameter is NOT a dict")
    if len(stream) == len(set(stream)):
        return True
    else:
        return False
    # if i in tweets.data.text.is_match() 

def scrape_timeline(expansions):
    stream = get_timeline(expansions)

    for tweet in stream.data:
        if is_duplicate(tweet.id) == True : 
           continue 
    return stream
    
    # check is same username is in timeline, if yes, check if tweet is the same exact.

def keyword_list(stream):
    #get the keys from object where object is a list of dicts
    return list(stream.data[0].keys())

def get_follower_count():
    return

def main():
    #define the data to be extracted
    expansions = ['author_id','referenced_tweets.id','referenced_tweets.id.author_id,entities.mentions.username','attachments.poll_ids']

    tweets = scrape_timeline(expansions)
    keys = keyword_list(tweets)
    print(keys) # return only 3 items since there is no expansion params
    print(tweets)
         # need to delete rules? after
    

if __name__ == '__main__':
    main()