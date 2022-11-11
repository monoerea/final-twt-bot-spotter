import tweepy
import configparser
import json
import sys
import pandas as pd

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

#PIN-based Authentication /3-legged
oauth1_user_handler = tweepy.OAuth1UserHandler(
    consumer_key=CONSUMER_KEY, consumer_secret= CONSUMER_SECRET,
    callback="oob")

auth_url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)
print(auth_url)

verifier = input("Input PIN: ")
access_token, access_token_secret = oauth1_user_handler.get_access_token(
    verifier
)

api = tweepy.API(oauth1_user_handler)

def export_json(myDict):
    json_object = json.dumps(myDict, indent=4)
    
    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

def convert_dict_to_df(myDict):
    
     #Convert from dictionary to DataFrame
    df = pd.DataFrame.from_dict(myDict) 
    #Output to csv file
    df.to_csv('response_python.csv',index = False, header=True)

process_status = {}

timeline = api.home_timeline(count = 10)
#for status in tweepy.Cursor(api.home_timeline).items():
    # process status here
#    process_status(status)
print(timeline._json)