import tensorflow as tf

print("TensorFlow versiyonu:", tf.__version__)
print("GPU kullanılabilir mi?:", tf.config.list_physical_devices('GPU'))
