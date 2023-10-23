import boto3
import os
import cv2

class Rekognition(object):
    def __init__(self, region_name='us-east-1'):
        self.client = boto3.client('rekognition', region_name=region_name)
        self.model = os.environ.get("REKOGNITION_MODEL_ARN")

    def show_custom_labels(self, image):     
        image_bytes = cv2.imencode('.jpg', image)[1].tobytes()
        response = self.client.detect_custom_labels(Image={'Bytes': image_bytes}, ProjectVersionArn=self.model)
        return response['CustomLabels'][0]['Name'], response['CustomLabels'][0]['Confidence']

    def inference(self, image_bytes):
        label_count, confidence = self.show_custom_labels(image_bytes)
        return label_count, confidence

