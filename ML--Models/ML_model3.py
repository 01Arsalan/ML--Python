import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing


df=pd.read_csv("Data-sets/teleCust1000t.csv")

print(df.head())

print(df.columns)

#['region', 'tenure', 'age', 'marital', 'address', 'income', 'ed','employ', 'retire', 'gender', 'reside', 'custcat']

x= df[['region', 'tenure', 'age', 'marital', 'address', 'income', 'ed',
       'employ', 'retire', 'gender', 'reside']].values

print(x[0:5])

#['region', 'tenure', 'age', 'marital', 'address', 'income', 'ed','employ', 'retire', 'gender', 'reside']

#converting df into arrays

#creating dependent variable ---y

y=df["custcat"].values

print(y[0:5])

#normalization
#standardization scaling
x= preprocessing.StandardScaler().fit(x).transform(x.astype(float))

print(x[0:5])


#train test split (out of test accuracy)--is a percentage of current

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)

#chaecking data shape

print("\n\ntrain set : ,", x_train.shape,y_train.shape)
print("test set : ,", x_test.shape,y_test.shape)


#creating classifier (KNN)

from sklearn.neighbors import KNeighborsClassifier

# training

k=110

neigh=KNeighborsClassifier(n_neighbors=k).fit(x_train,y_train)

print(neigh)


#predicting
y_pred=neigh.predict(x_test)

print(y_pred[0:5])

#accuracy
from sklearn.metrics import accuracy_score

print("\n\nAccuracy : ",accuracy_score(y_test,y_pred))

