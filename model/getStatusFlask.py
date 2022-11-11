import tweepy
import json
import sys
import pandas as pd
import numpy as np
from csv import DictWriter
import configparser

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
auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

API = tweepy.API(auth)
    # data I need to exteract
    #data I will recieve 

def extract_screen_name(requestJson):
    screen_name = []
    requestJson = json.loads(requestJson)
    for each in range(len(requestJson)):
        screen_name.append(requestJson[each]['screen_name']) # CRITICAL NEEDS 
    print(screen_name)
    return screen_name
def get_by_screenName(screen_name):
    return API.get_status(screen_name = screen_name,)._json

def convert_dict_to_df(myDict, filename): # modify/ split csv and filepath from filename
    df = pd.DataFrame.from_dict(myDict, orient='index').T
    df.to_csv(filename,index = False, header=True)
def convert_list_to_df(myDict, filename): # modify/ split csv and filepath from filename
    df = pd.DataFrame.from_dict(myDict,  orient='index')
    df.to_csv(filename,index = False)

def Obj_to_dict(myObj):
    myObj.update(myObj._json.items())
    return myObj 
def get_features(myObj,num,mainKey,key):
    return len(myObj[num][mainKey].get(key))
def get_status_dict(screen_name,count):
    return API.user_timeline(screen_name = screen_name, count = count, include_rts = False)
def getStatus(requestJson,count):
    count = count
    nameList = extract_screen_name(requestJson)
    #ERROR: MIGHT STORE ONLY 1 value
    myRange = len(nameList)
    store = []
    notFound = [] #store deleted accounts
    for x in nameList:
        for status in range(count):
            try:
                store.append(get_status_dict(x,count)[status]._json)
                print(store)
                print
            except:
                print(x, sys.exc_info())
                notFound.append(x)
    #GET KEYS FROM RESPONSE OBJECT
    keys = ['hashtags','symbols','user_mentions','urls']
    mainKeys = ['count_hashtags','count_symbols','count_user_mentions','count_urls']
    userObj =[] #initialize dict
    #Append keys and empty list to DICT
    '''for i in keys:
        userObj.__setitem__(i,[])'''

    num = range(myRange-len(notFound))
    for j in num:
        for i in keys:
            userObj.append(get_features(store,j,'entities',i))
            #userObj.append(store[j]['entities'].get(i))
    myDict = to_numpy_array(userObj)
    # convert_list_to_df(myDict, 'data/accInfo_list.csv')
    return myDict
    #print(notFound)
def to_numpy_array(myDict):
    #myDict = myDict.items()
    myDict = list(myDict)
    myArray = [np.array(myDict)]
    #myDict.flatten()
    print(myArray)
    return myArray

def main():
    #for Testing code
    with open('data/json/oneuser.json', 'r') as data_file:
        userList = data_file.read()
    getStatus(userList,2)
if __name__ == '__main__':
    main()