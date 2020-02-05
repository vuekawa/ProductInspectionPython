from __future__ import absolute_import, division, print_function, unicode_literals
import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
import pathlib


keras = tf.keras
AUTOTUNE = tf.data.experimental.AUTOTUNE
default_timeit_steps = 1000

def get_label(file_path):
    # convert the file_path to a list of path components in a TENSOR format
    parts = tf.strings.split(file_path, os.path.sep)
    # the second to last is the class-directory
    return parts[-2] == CLASS_NAMES

def convert_to_png(directory):
    for folder in os.listdir(directory):
        for image in directory.glob(folder + "/*.bmp"):
            im = Image.open(image)
            name = im.filename
            im.save(name[:-4]+".png")
            im.close()
            os.remove(name)
    
def decode_img(img):
    img = tf.image.decode_png(img, channels=3)
    img = tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT])
    img = tf.image.convert_image_dtype(img, tf.float32)
    
    return img

def process_path(file_path):
    label = get_label(file_path)
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label

def prepare_for_training(ds, cache = True, shuffle_buffer_size = 1000):
    if cache:
        if isinstance(cache, str):
            ds = ds.cache(cache)
        else:
            ds = ds.cache()
    
    ds = ds.shuffle(buffer_size = shuffle_buffer_size)
    
    ds = ds.repeat()
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(buffer_size = AUTOTUNE)
    return ds

def show_batch(image_batch, label_batch):
  plt.figure(figsize=(10,10))
  for n in range(25):
      plt.subplot(5,5,n+1)
      plt.imshow(image_batch[n])
      plt.title(CLASS_NAMES[label_batch[n]==1][0].title())
      plt.axis('off')
    
if __name__ == "__main__":
    # Read images from folder
    np.random.seed(42)
    data_dir = pathlib.Path("C:/Users/pdel96/Desktop/Classification_Sample/multiclass0120")
    convert_to_png(data_dir)
    img_count = len(list(data_dir.glob('*/*.png')))
    CLASS_NAMES = np.array([item.name for item in data_dir.glob('*')])

    # Load the files as dataset
    list_ds = tf.data.Dataset.list_files(str(data_dir/'*/*.png'))
    
    # Define parameters for the dataset    
    BATCH_SIZE = 32
    IMG_HEIGHT = 224
    IMG_WIDTH = 224
    
    labeled_ds = list_ds.map(process_path, num_parallel_calls = AUTOTUNE)
    
    training_percent = 0.80
    validation_percent = 0.15
    
    train_set = labeled_ds.take(np.ceil(img_count*training_percent))
    val_set = labeled_ds.skip(np.ceil(img_count*training_percent))
    test_set = labeled_ds.skip(np.ceil(img_count*validation_percent))
    val_set = labeled_ds.take(np.ceil(img_count*validation_percent))
    
    train_batches = prepare_for_training(train_set)
    val_batches = val_set.batch(BATCH_SIZE)
    test_batches = test_set.batch(BATCH_SIZE)
    
    STEPS_PER_EPOCH = np.ceil(img_count*training_percent/BATCH_SIZE)
    
    IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH, 3)
        
    base_model = tf.keras.applications.ResNet50(weights = 'resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5', include_top = False, input_shape = IMG_SHAPE)
    base_model.trainable = False
    
    
    #global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
    #drop_out_layer = tf.keras.layers.Dropout(0.5)
    intermediate_layer = tf.keras.layers.Dense(units = 128, activation = "relu")
    drop_out_layer2 = tf.keras.layers.Dropout(0.5)
    intermediate_layer2 = tf.keras.layers.Dense(units = 64, activation = "relu")
    output_layer = tf.keras.layers.Dense(units = 4, activation = "softmax")
    
    tl_model = tf.keras.Sequential([
            base_model,
            #global_average_layer,
            #drop_out_layer,
            intermediate_layer,
            drop_out_layer2,
            intermediate_layer2,
            output_layer])
    tl_model.summary()
    
    
    
#    tl_model.compile(optimizer = tf.keras.optimizers.SGD(),
#                     loss = "sparse_categorical_crossentropy",
#                     metrics = ["accuracy"])
#    callbacks = [tf.keras.callbacks.TensorBoard(log_dir = ".\\log\\transfer_learning_model\\", update_freq = "batch")]
#    tl_model.fit(train_ds, epochs = 100, validation_data = val_ds, validation_freq = 1, callbacks = callbacks)
    
#    tl_model.compile(optimizer = tf.keras.optimizers.Adam(lr = 0.0001),
#                     loss = "categorical_crossentropy",
#                     metrics = ["accuracy"])
#    callbacks = [tf.keras.callbacks.TensorBoard(log_dir = ".\\log\\transfer_learning_model\\", update_freq = "batch")]
#    #tl_model.fit(train_ds, steps_per_epoch = STEPS_PER_EPOCH, epochs = 100, validation_data = val_ds, validation_steps = 10, callbacks = callbacks)
#    tl_model.fit(train_ds, epochs = 10, validation_data = val_ds, callbacks = callbacks)
    
    
    tl_model.compile(optimizer = tf.keras.optimizers.SGD(lr = 0.0001, momentum = 0.9),
                     loss = "categorical_crossentropy",
                     metrics = ["categorical_accuracy"])
    callbacks = [tf.keras.callbacks.TensorBoard(log_dir = ".\\log\\transfer_learning_model\\", update_freq = "batch")]
    #tl_model.fit(train_ds, steps_per_epoch = STEPS_PER_EPOCH, epochs = 100, validation_data = val_ds, validation_steps = 10, callbacks = callbacks)
    tl_model.fit(train_batches, steps_per_epoch = STEPS_PER_EPOCH, epochs = 100, validation_data = val_batches, callbacks = callbacks)