import tensorflow as tf

from tensorflow.python.client import device_lib
gpu_devices = tf.config.list_physical_devices('GPU')
all_devices = device_lib.list_local_devices()

for device in all_devices: 
    print("==============\nDevice =", device.physical_device_desc)

print("==============\nNumber of GPU =", len(gpu_devices)) 

print("TensorFlow built with CUDA =",tf.test.is_built_with_cuda())

#print("Devices:")
#for device in tf.config.get_visible_devices():
#    print(device)

