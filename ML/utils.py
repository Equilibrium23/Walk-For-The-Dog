import tensorflow as tf
import pandas as pd
import cv2
import numpy as np

labels_df = pd.read_csv("ML/labels.csv")
breeds = labels_df["breed"].unique()
id2breed = {i: name for i, name in enumerate(breeds)}
model = tf.keras.models.load_model("ML/modelV3.h5")


def read_image(path, size):
    image = cv2.imread(path)
    image = cv2.resize(image, (size, size))
    image = image / 255.0
    image = image.astype(np.float32)
    return image


def make_prediction(path, size):
    image = read_image(path, size)
    image = np.expand_dims(image, axis=0)
    y_pred = model.predict(image)[0]
    label_idx = np.argmax(y_pred)
    return id2breed[label_idx]