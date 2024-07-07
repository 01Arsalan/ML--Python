import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

_URL="https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip"                    
zip_dir=tf.keras.utils.get_file("cats_and_dogs_filtered.zip", origin=_URL, extract=True)  

base_dir= os.path.join(os.path.dirname(zip_dir),'cats_and_dogs_filtered')                           

train_dir=os.path.join(base_dir,'train')
validation_dir=os.path.join(base_dir,"validation")

train_cats_dir=os.path.join(train_dir,"cats")
train_dogs_dir=os.path.join(train_dir,"dogs")
validation_cats_dir=os.path.join(validation_dir,"cats")
validation_dogs_dir=os.path.join(validation_dir,"dogs")

cats_train=len(os.listdir(train_cats_dir))
cats_val=len(os.listdir(validation_cats_dir))
dogs_train=len(os.listdir(train_dogs_dir))
dogs_val=len(os.listdir(validation_dogs_dir))

total_train=cats_train+dogs_train
total_val=cats_val+dogs_val

print("Total cat images to train    : ",cats_train,"\nTotal cat images to validate : ",cats_val)
print("Total dog images to train    : ",dogs_train,"\nTotal dog images to validate : ",dogs_val)


from tensorflow.keras import layers
from tensorflow.keras import Model

from keras.layers import Conv2D,MaxPooling2D,\
     Dropout,Flatten,Dense,Activation,\
     BatchNormalization

model=tf.keras.Sequential()

model.add(Conv2D(16,(3,3),activation='relu',input_shape=(150,150,3)))
model.add(MaxPooling2D(pool_size=(2,2)))


model.add(Conv2D(32,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))


model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(128,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1,activation='sigmoid'))

from tensorflow.keras.optimizers import RMSprop

model.compile(loss='binary_crossentropy',optimizer=RMSprop(lr=0.001),metrics=['acc'])



train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        train_dir,  
        target_size=(150, 150),  
        batch_size=20,
        class_mode='binary')

validation_generator = val_datagen.flow_from_directory(
        validation_dir,
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')


def plot_images(images_arr):
  fig,axes=plt.subplots(1,5,figsize=(20,20))
  axes=axes.flatten()
  for img, ax in zip(images_arr,axes):
    ax.imshow(img)
  plt.tight_layout()
  plt.show()

augmented_images=[train_generator[0][0][0] for i in range(5)]
plot_images(augmented_images)


Epochs=100
history = model.fit_generator(
      train_generator,
      steps_per_epoch=100,  
      epochs=Epochs,
      validation_data=validation_generator,
      validation_steps=50,  
      verbose=2
      )


loss = history.history['loss']
acc = history.history['acc']
plt.plot(acc,label='Accuracy',c='r')
plt.plot(loss,label='Loss',c='b')
plt.title('Accuracy and Loss')
plt.legend()
plt.show()

v_loss = history.history['val_loss']
v_acc = history.history['val_acc']
plt.plot(v_acc,label='Val_Accuracy',c='r')
plt.plot(v_loss,label='Val_Loss',c='b')
plt.title('Validation Accuracy and Loss')
plt.legend()
plt.show()


model.save('Cat_Dog.hdf5')