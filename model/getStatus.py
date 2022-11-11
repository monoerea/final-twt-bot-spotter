
#WORKING

import tweepy
import keys
import json
import sys
import pandas as pd
from csv import DictWriter
sys.stdout.reconfigure(encoding='utf-8')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key=keys.CONSUMER_KEY, consumer_secret=keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

API = tweepy.API(auth)
##GLOBALS
count = 1
myRange = 300
myDict = {}

def fitStatus():
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    data_set=pd.read_csv('data/cleaned_statusInfo.csv') 
    '''Extracting Independent and dependent Variable'''  
    x = data_set[['count_hashtags','count_symbols','count_user_mentions','count_urls']]
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
    joblib.dump(classifier, 'data/classifier_statusInfo.pkl')

def cleanStatus():
    dataset1 = pd.read_csv('data/label.csv',nrows=myRange)
    dataset1 = dataset1.replace({'id':{'u':''}}, regex=True)
    dataset1 = dataset1.astype({'id':'int64'})
    print(dataset1)
    print("+++++++++++++++++++++++++++")
    dataset2 = pd.read_csv('data/statusInfo.csv',nrows=myRange)
    print(dataset2)
    print("---------------------------")
    mergedDataset = pd.merge(dataset1,dataset2, left_on='id',right_on="userid")
    #print(mergedDataset)
    #mergedDataset = dataset1.merge(dataset2, on='id')
    #dataset3 = pd.read_csv('data/statusInfo.csv',nrows=myRange)
    #dataset3 = dataset3['entities']
    mergedDataset.to_csv('data/cleaned_statusInfo.csv',index=False)
    #print(mergedDataset)

#export dicts to json file
def export_json(myDict):
    json_object = json.dumps(myDict, indent=4)
    
    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
#exports dict to csv file
def convert_dict_to_df(myDict):
     #Convert from dictionary to DataFrame
    df = pd.DataFrame.from_dict(myDict, orient='index').T
    #Output to csv file
    df.to_csv('data/statusInfo.csv',index = False, header=True)
    
def Obj_to_dict(myObj):
    myDict.update(myObj._json.items())
    return myDict

#get status of each passed user/ returns a response object
def get_status_dict(uid):
    return API.user_timeline(user_id = uid, count = count, include_rts = False)

#removes 'u' from uid
def clean_csv(file):
    dataset = pd.read_csv(file,nrows=myRange)
    finaldataset = dataset['id']
    finaldataset = finaldataset.replace({'u':''}, regex=True)
    return finaldataset

def getStatus():
    #define the data to be extracted
    expansions = ['author_id','referenced_tweets.id','referenced_tweets.id.author_id,entities.mentions.username','attachments.poll_ids']
    
    uid = clean_csv('data/label.csv')
    store = []
    storeEntities = {'id':[],'hashtags':[],'symbols':[],'user_mentions':[],'urls':[],'count_hashtags':[],'count_symbols':[],'count_user_mentions':[],'count_urls':[]}
    storeUser = {'id':[],'userid':[]}
    notFound = [] #store deleted accounts
    for x in uid[:myRange]:
        for status in range(count):
            try:
                store.append(get_status_dict(x)[status]._json)
            except:
                print(x, sys.exc_info())
                notFound.append(x)

    for y in range(len(store)):
        storeEntities['id'].append(store[y]['id'])
        storeEntities['hashtags'].append(store[y]['entities']['hashtags'])
        storeEntities['symbols'].append(store[y]['entities']['symbols'])
        storeEntities['user_mentions'].append(store[y]['entities']['user_mentions'])
        storeEntities['urls'].append(store[y]['entities']['urls'])
        storeEntities['count_hashtags'].append(len(store[y]['entities']['hashtags']))
        storeEntities['count_symbols'].append(len(store[y]['entities']['symbols']))
        storeEntities['count_user_mentions'].append(len(store[y]['entities']['user_mentions']))
        storeEntities['count_urls'].append(len(store[y]['entities']['urls']))
        storeUser['id'].append(store[y]['id'])
        storeUser['userid'].append(store[y]['user']['id'])
    #GET KEYS FROM RESPONSE OBJECT
    keys = list(store[0].keys())
    #print(store[0].get(keys))
    
    myObject ={} #initialize dict
    #Append keys and empty list to DICT
    for i in keys:
        myObject.__setitem__(i,[])
    print(myObject)
    #
    num = range(myRange*count-len(notFound))
    for j in num:
        for i in keys:
            myObject[i].append(store[j].get(i))
    
    myObject = pd.DataFrame.from_dict(myObject)
    storeEntities = pd.DataFrame.from_dict(storeEntities)
    storeUser = pd.DataFrame.from_dict(storeUser)

    myObject = myObject.merge(storeEntities, on='id')
    myObject = myObject.merge(storeUser, on="id")
    
    convert_dict_to_df(pd.DataFrame.to_dict(myObject))
    print(notFound)

def main():
    getStatus()
    cleanStatus()
    fitStatus()
    
if __name__ == '__main__':
    #get User data and exports to CSV
    main()

