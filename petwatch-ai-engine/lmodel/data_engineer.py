import os
import cv2
import cvlib as cv
from cvlib.object_detection import YOLO
import threading

class ExtractorThread(threading.Thread):
    def __init__(self, source, label, nome_do_gato, folder):
        threading.Thread.__init__(self)
        self.source = source
        self.label = label
        self.nome_do_gato = nome_do_gato
        self.folder = folder
        weights = "lmodel/yolov4.weights"
        config = "lmodel/yolov4.cfg"
        labels = "lmodel/yolov3_classes.txt"
        self.yolo = YOLO(weights, config, labels)
        print("cheguei")

    def run(self):
        video = cv2.VideoCapture(self.source)
        frame_count = 0

        while video.isOpened():
            status, frame = video.read()
            if not status:
                break

            bbox, detected_labels, conf = self.yolo.detect_objects(frame)
            print(detected_labels)

            for l, c in zip(detected_labels, conf):
                if l == self.label:
                    idx = detected_labels.index(l)
                    x, y, x2, y2 = map(int, bbox[idx])

                    if x >= 0 and y >= 0 and x2 >= 0 and y2 >= 0:
                        cropped = frame[y:y2, x:x2]

                        if cropped.any():
                            if not os.path.exists(self.folder):
                                os.makedirs(self.folder)
                            output_path = os.path.join(self.folder, f"{self.nome_do_gato}_{frame_count}.jpg")
                            cv2.imwrite(output_path, cropped)
                            frame_count += 1
                            print(frame_count)

        video.release()
