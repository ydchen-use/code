#!/usr/bin/env python
import tensorflow as tf

from tensorflow import keras
from tensorflow.python.keras import layers
import numpy as np
import time

tf.compat.v1.disable_eager_execution()

# 查看是否有可用的GPU
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))


tf.config.set_soft_device_placement(True)
tf.debugging.set_log_device_placement(True)

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)

t = time.time()
with tf.device("/gpu:0"):
    tf.random.set_seed(0)
    a = tf.random.uniform((10000,10000),minval = 0,maxval = 3.0)
    c = tf.matmul(a, tf.transpose(a))
    d = tf.reduce_sum(c)
print('gpu: ', time.time()-t)

t = time.time()
with tf.device("/cpu:0"):
    tf.random.set_seed(0)
    a = tf.random.uniform((10000,10000),minval = 0,maxval = 3.0)
    c = tf.matmul(a, tf.transpose(a))
    d = tf.reduce_sum(c)
print('cpu: ', time.time()-t)


a = tf.constant(1.)
b = tf.constant(2.)
print(a + b)
print("GPU: ", tf.config.list_physical_devices("GPU"))
print(tf.__version__)

