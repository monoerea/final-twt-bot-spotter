import pandas as pd

dataset1 = pd.read_csv('data/label.csv')
dataset1 = dataset1.replace({'id':{'u':''}}, regex=True)

print(type(dataset1))
'''
dataset1 = dataset1.astype({'id':'int64'})
dataset2 = pd.read_csv('data/statusInfo.csv')
mergedDataset = dataset1.merge(dataset2, on='id')

#dataset3 = dataset3['entities']
#mergedDataset.to_csv('data/cleaned_statusInfo.csv',index=False)
dataset3 = dataset3['entities'].to_dict()
print(dataset3)
print(dataset3.keys())
print(dataset3.values())
for x in dataset3:
    print(x)

'''