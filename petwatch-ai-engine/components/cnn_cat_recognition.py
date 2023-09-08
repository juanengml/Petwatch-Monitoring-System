# cat_recognition.py

from keras.models import load_model
import numpy as np
import cv2

class CatRecognitionModel:
    def __init__(self, model_path, labels_path):
        self.model = load_model(model_path, compile=False)
        self.class_names = open(labels_path, "r").readlines()

    def preprocess_image(self, image_array):
        # Preprocess the image array
        print(image_array.shape)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        normalized_image_array = cv2.resize(normalized_image_array, (224, 224))
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array
        return data

    def predict(self, image_data):
        # Make a prediction
        prediction = self.model.predict(image_data)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]
        return class_name[2:], confidence_score
