# creating a digit recognition Deep Learning model.

from sklearn.metrics import accuracy_score
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data(path="mnist.npz")  # Downloading Data Set

print(x_train.shape)

labels='zero one two three four five six seven eight nine ten'
labels=labels.split()
labels


plt.imshow(x_train[0], cmap='gray')                                                         # image view
plt.show()

np.unique(y_train, return_counts=True)

x_train[0].max()
x_train[0].min()
# image normalization 
x_train = x_train/255
x_test = x_test/255

# Neural Network Architechture

model = tf.keras.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=x_train[0].shape))                # (28*28 neurons)
model.add(tf.keras.layers.Dense(1568, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))


model.summary()

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['accuracy']) #back propogation

model.fit(x_train, y_train, epochs=2)

loss = pd.DataFrame(model.history.history['loss']).plot()
accuracy = pd.DataFrame(model.history.history['accuracy']).plot()


y_pred = model.predict(x_test)
y_pred = np.argmax(y_pred, axis=1)
print(y_pred)

print(y_test)

accuracy_score(y_test, y_pred)

np.unique(y_pred, return_counts=True)

np.unique(y_test, return_counts=True)

model.save('Num_Rec.hdf5')
