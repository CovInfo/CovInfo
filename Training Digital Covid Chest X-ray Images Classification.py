from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import cv2
import os

'''img = image.load_img(r"D:\Contactless Covid Detection\Xrays\archive\COVID-19_Radiography_Dataset\Dataset\COVID\COVID-1.png")
plt.imshow(img)
a = cv2.imread(r"D:\Contactless Covid Detection\Xrays\archive\COVID-19_Radiography_Dataset\Dataset\COVID\COVID-1.png")
print(a.shape)'''

# Preprocessing & training the data

train = ImageDataGenerator(rescale=(1 / 255))
train_dataset = train.flow_from_directory(
    'D:/Contactless Covid Detection/Xrays/archive/COVID-19_Radiography_Dataset/Dataset',
    target_size=(299, 299),
    batch_size=3,
    class_mode='binary')

# Making Deep Learning Model

NAME = "MODEL100"
model = tf.keras.models.Sequential([tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(299, 299, 3)),
                                    tf.keras.layers.MaxPool2D(2, 2),
                                    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
                                    tf.keras.layers.MaxPool2D(2, 2),
                                    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                                    tf.keras.layers.MaxPool2D(2, 2),
                                    tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(512, activation='relu'),
                                    tf.keras.layers.Dense(1, activation='sigmoid')])

model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['accuracy'])
model.summary()

model.fit(train_dataset,
          steps_per_epoch=10,
          batch_size=32,
          epochs=100,
         )

model.save("xray_covid_model.h5")
