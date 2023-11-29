import cv2
import base64
import numpy as np
from ultralytics import YOLO as YOLOV8

result_inference = {
                "cropped": None,
                "label": "",
                "bbox": {"x": "", "y": "", "x2": "", "y2": ""}
            }

# Load a pretrained YOLOv8n model
class LoadModel(object):
  def __init__(self, model_path): # '/content/runs/detect/train/weights/best.pt'
      self.model = YOLOV8(model_path)

  def inference(self, image): #
      return self.model.predict(image)

  def get_model(self):
      return self.model

model_inference = LoadModel('lmodel/best.pt')

def inference_yolo(frame):
    results_list = []

    results = model_inference.inference(frame)
    
    for result in results:
        box = result.boxes  # Boxes object for bbox outputs
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        class_id = result.names[box.cls[0].item()]
        conf = round(box.conf[0].item(), 2)

        x, y, x2, y2 = cords

        result_dict = {
            'label': class_id,
            'bbox': {'x': x, 'y': y, 'x2': x2, 'y2': y2},
            'confidence': conf
        }

        results_list.append(result_dict)

    return results_list[0]


def decode_base64_to_byarray(foto_base64):
    foto_bytes = base64.b64decode(foto_base64)
    image_array = np.frombuffer(foto_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image