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
'''
    [
    {screen_name:value,datetime:value},
    {screen_name:value,datetime:value},
    ]
    '''
def extract_screen_name(requestJson):
    screen_name = []
    requestJson = json.loads(requestJson)
    for each in range(len(requestJson)):
        screen_name.append(requestJson[each]['screen_name']) # CRITICAL NEEDS 
    print(screen_name)
    return screen_name
def get_by_screenName(screen_name):
    return API.get_user(screen_name = screen_name)._json

def convert_dict_to_df(myDict, filename): # modify/ split csv and filepath from filename
    df = pd.DataFrame.from_dict(myDict, orient='index').T
    df.to_csv(filename,index = False, header=True)
def convert_list_to_df(myDict, filename): # modify/ split csv and filepath from filename
    df = pd.DataFrame.from_dict(myDict,  orient='index')
    df.to_csv(filename,index = False)

def Obj_to_dict(myObj):
    myObj.update(myObj._json.items())
    return myObj 

def get_statusCount(user,userList):
        return userList[user].status_count.values()
def getUser(requestJson):
    nameList = extract_screen_name(requestJson)
    #ERROR: MIGHT STORE ONLY 1 value
    myRange = len(nameList)
    store = []
    notFound = [] #store deleted accounts
    for x in nameList[:myRange]:
        try:
            store.append(get_by_screenName(x))
        except:
            print(x, sys.exc_info()[0])
            notFound.append(x)
    #GET KEYS FROM RESPONSE OBJECT
    keys = ['statuses_count','default_profile','default_profile_image','verified','favourites_count','followers_count','friends_count','listed_count']
    userObj =[] #initialize dict
    #Append keys and empty list to DICT
    '''for i in keys:
        userObj.__setitem__(i,[])'''

    num = range(myRange-len(notFound))
    for j in num:
        for i in keys:
            userObj.append(store[j].get(i))
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
    getUser(userList)
if __name__ == '__main__':
    main()