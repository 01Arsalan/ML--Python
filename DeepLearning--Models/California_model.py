#Regeression model--(neural network to predict housing price)

#Datase : calafornia housing dataset.

from sklearn.datasets import fetch_california_housing as ds
house= ds()

type(house)   #bunch as simialar as a dictioary(key : value)

house.keys()

print(house['DESCR'])     #similar to df.info()

#creating a data frame out of this sklearn.bunch
import pandas as pd
df=pd.DataFrame(house["data"],columns=house['feature_names'])   #column names are in house["feature_names"]
df["target"]=house["target"]      #adding target column to df
df

# step 2 : split the data into input and output

x=df.iloc[:,0:6].values
y=df.iloc[:,-1].values

# step 3 : divide the data into test and train data(75:25)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=0)# test_size=0.25()default,

print(x_train.shape,x_test.shape,y_train.shape,y_test.shape)



#scaling the data# use(std scaler or min max scaler), for images dive by 255
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
x_train=scaler.fit_transform(x_train)
x_test=scaler.transform(x_test)


#creaating a simple neural network( one hidden layer)

import tensorflow as tf

model=tf.keras.Sequential()
model.add(tf.keras.layers.Dense(5,activation = 'relu',input_shape=x_train[0].shape))
model.add(tf.keras.layers.Dense(1))


#back propogation
model.compile(optimizer="adam",loss="mean_squared_error")

model.summary()

model weightsmodel.get_weights()


model.fit(x_train,y_train,epochs=20)


#prdicting values
y_pred=model.predict(x_test)

#checking accuracy using(MSE)
from sklearn.metrics import mean_squared_error #should be as close to zero as possible
mean_squared_error(y_test,y_pred)

 #0.5011348454613426



