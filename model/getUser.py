
#WORKING
import tweepy
import configparser
import json
import sys
import pandas as pd
from csv import DictWriter
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
auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)

myDict = {}
myRange = 300#change here to increase training/testing size 
def fitUser():
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    data_set=pd.read_csv('data/cleaned_accInfo.csv') 
    '''Extracting Independent and dependent Variable'''  
    x = data_set[['statuses_count','default_profile','default_profile_image','verified','favourites_count','followers_count','friends_count','listed_count']]
    y = data_set['label']
    print(x)
    ''' Splitting the dataset into training and test set.''' 
    from sklearn.model_selection import train_test_split  
    x_train, x_test, y_train, y_test= train_test_split(x, y, test_size=.75,random_state=0)
    '''feature Scaling
    from sklearn.preprocessing import StandardScaler    
    st_x= StandardScaler()    
    x_train= st_x.fit_transform(x_train)    
    x_test= st_x.transform(x_test)'''
    '''Fitting Decision Tree classifier to the training set '''
    from sklearn.ensemble import RandomForestClassifier  
    classifier= RandomForestClassifier(n_estimators= 10, criterion="entropy")  
    #classifier=RandomForestClassifier()
    classifier.fit(x_train, y_train)  
    '''Predicting the test set result'''  
    y_pred= classifier.predict(x_test)  
    print(x_test)
    print(y_pred)
    '''Creating the Confusion matrix '''
    from sklearn.metrics import confusion_matrix  
    cm= confusion_matrix(y_test, y_pred)  
    print(cm)
    '''Exporting the trained tree'''
    #import pickle
    #pickle.dump(classifier, open("classifier.pkl", "wb"))
    import joblib
    joblib.dump(classifier, 'data/classifier_accInfo.pkl')

def cleanUser():
    dataset1 = pd.read_csv('data/label.csv',nrows=myRange)
    dataset1 = dataset1.replace({'id':{'u':''}}, regex=True)
    dataset1 = dataset1.astype({'id':'int64'})
    dataset2 = pd.read_csv('data/accInfo.csv',nrows=myRange)
    mergedDataset = dataset1.merge(dataset2, on='id')
    mergedDataset.to_csv('data/cleaned_accInfo.csv',index=False)
    print(mergedDataset)
    
def convert_dict_to_df(myDict):
    df = pd.DataFrame.from_dict(myDict, orient='index').T
    df.to_csv('data/accInfo.csv',index = False, header=True)

def Obj_to_dict(myObj):
    myDict.update(myObj._json.items())
    return myDict
    
def get_user_dict(uid):
    return API.get_user(user_id = uid)._json

def clean_csv(file):
    dataset = pd.read_csv(file,nrows=myRange)
    finaldataset = dataset['id']
    finaldataset = finaldataset.replace({'u':''}, regex=True)
    return finaldataset

def getUser():
    #define the data to be extracted
    uid = clean_csv('data/label.csv')
    store = []
    storeLabel = []
    notFound = [] #store deleted accounts
    for x in uid[:myRange]:
        try:
            store.append(get_user_dict(x))
            storeLabel.append(x)
        except:
            print(x, sys.exc_info()[0])
            notFound.append(x)
    #GET KEYS FROM RESPONSE OBJECT
    keys = store[0].keys()
    #print(store[0].get(keys))
    
    userObj ={} #initialize dict
    #Append keys and empty list to DICT
    for i in keys:
        userObj.__setitem__(i,[])
    #print(userObj)
    #
    num = range(myRange-len(notFound))
    for j in num:
        print(j)
        for i in keys:
            userObj[i].append(store[j].get(i))
    convert_dict_to_df(userObj)
    #print(notFound)

def main():
    getUser()
    cleanUser()
    fitUser()

if __name__ == '__main__':
    #get User data and exports to CSV
    main()
