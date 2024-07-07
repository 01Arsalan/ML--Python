#(Problem Type: Regression)
#(Calafornia Housing Dataset)

from optparse import Values
from sklearn.datasets import fetch_california_housing

house=fetch_california_housing()
# print(house.keys())

import pandas as pd

df=pd.DataFrame(house['data'],columns=house['feature_names'])       # Creating a Data Frame
df["Target"]=house['target']
# print(df)

x=df.iloc[:,0:6].values                                             # Spliting Data Frame into input and output
y=df.iloc[:,-1].values

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=0) # Spliting data into Train and Test | Default : 75/25

# print(x_test.shape)

from sklearn.preprocessing import StandardScaler                    # Scaling (we use std scalar || min max sacalar ||| for images we divide by 255)
scaler=StandardScaler()
x_train=scaler.fit_transform(x_train)
x_test=scaler.transform(x_test)


# neural network of 1 hidden layer

import tensorflow as tf
model=tf.keras.Sequential()                                                          # Beginner level API
model.add(tf.keras.layers.Dense(5,activation="relu",input_shape=x_train[0].shape))   # Adding 5 neurons to hidden layer
model.add(tf.keras.layers.Dense(1))                                                  # Adding 1 neuron to output layer

# print(model.summary())

model.compile(optimizer="adam",loss="mean_squared_error")

model.fit(x_train,y_train,epochs=2)

y_pred=model.predict(x_test)

from sklearn.metrics import mean_squared_error
acc=mean_squared_error(y_test,y_pred)
print(acc)
