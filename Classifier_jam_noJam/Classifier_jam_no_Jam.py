import numpy as np
#from keras.models import Model
#from keras.preprocessing import image
#from keras.applications import imagenet_utils, mobilenet
import tensorflow as tf
#sess = tf.Session(config=tf.ConfigProto(log_device_placement=True)) #check for gpu
import matplotlib.pyplot as plt
import os
import cv2

Jam_images_files = os.listdir('./Jam')
Jam_images = np.zeros((len(os.listdir('./Jam')),299,299,3))

for i in range(len(Jam_images_files)):
    Jam_images[i] = cv2.resize(1.*plt.imread('./Jam/'+Jam_images_files[i])/255,
                                (299,299))

NotJam_images_files = os.listdir('./notJam')
NotJam_images = np.zeros((len(os.listdir('./notJam')),299,299,3))

for i in range(len(NotJam_images_files)):
    NotJam_images[i] = cv2.resize(1.*plt.imread('./notJam/'+NotJam_images_files[i])/255,
                                  (299,299))

X = np.concatenate([Jam_images, NotJam_images],0)
y = np.array([1,]*len(Jam_images_files )+[0,]*len(NotJam_images_files ))


tf.keras.backend.set_learning_phase(0) #freeze batch norm

#v2 has bug savign model
# issue here https://github.com/tensorflow/tensorflow/issues/22697
mobilenetv2 = tf.keras.applications.InceptionV3(input_shape=(299,299,3),include_top=False)

for layer in mobilenetv2.layers:
    layer.trainable = False
final_layer =tf.keras.layers.GlobalAveragePooling2D()(mobilenetv2.output)
logits = tf.keras.layers.Dense(1,'sigmoid')(final_layer)
model = tf.keras.models.Model(inputs=mobilenetv2.input,outputs=logits)
#print (model.summary())
model.compile(loss='binary_crossentropy', optimizer=tf.train.AdamOptimizer(), metrics=['accuracy'])
train = np.array([i for i in range(len(X)) if i%5!=0])
val = np.array([i for i in range(len(X)) if i%5==0])
X_tr = X[train]
X_val = X[val]
y_tr = y[train]
y_val = y[val]

datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    featurewise_center=0,
    featurewise_std_normalization=0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)
model.fit_generator(datagen.flow(X_tr,y_tr,5),epochs=30,verbose=2,validation_data = (X_val,y_val))
print (model.evaluate(X_val,y_val,40))
#pred = model.predict(X,40)
pred = model.predict(X_val,40)
from sklearn.metrics import roc_auc_score
print roc_auc_score(y_val,pred)
model.save('keras_model.h5')
output_path = tf.contrib.saved_model.save_keras_model(model, './tmp_dir')

loaded_model = tf.contrib.saved_model.load_keras_model(output_path)

if True:
    from tensorflow.contrib import lite
    converter = lite.TFLiteConverter.from_keras_model_file( 'keras_model.h5')
    tfmodel = converter.convert()
    open ("graph.flite" , "wb") .write(tfmodel)
