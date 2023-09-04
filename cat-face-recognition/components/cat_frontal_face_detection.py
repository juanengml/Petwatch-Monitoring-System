#! /usr/bin/env python
"""
Use the pre-trained Haar classifier from OpenCV to detect cat faces
"""

import cv2
import dlib
import numpy as np
from constants.constants import debug_cat_frontal_face_detection


# pre-trained classifier from OpenCV
HAAR_CLASSIFIER = 'data/haarcascade_frontalcatface.xml'
DETECTOR = 'data/cat_face_detector.svm'
# Pre-trained shape predictor from iBUG 300-W dataset for human facial landmarks
SHAPE_PREDICTOR = 'data/cat_landmark_predictor.dat'

# finds landmarks in the form (from viewer perspective):
# index - (x,y)
MOUTH_INDEX = 0
LEFT_EYE_INDEX = 1
LEFT_EAR_LEFT_INDEX = 2
RIGHT_EAR_LEFT_INDEX = 3
NOSE_INDEX = 4
RIGHT_EYE_INDEX = 5
LEFT_EAR_RIGHT_INDEX = 6
RIGHT_EAR_RIGHT_INDEX = 7

detector = dlib.fhog_object_detector(DETECTOR)
#haar_detector = dlib.fhog_object_detector(HAAR_CLASSIFIER)
haar_detector = cv2.CascadeClassifier(HAAR_CLASSIFIER) 

landmarks_predictor = dlib.shape_predictor(SHAPE_PREDICTOR)


# convenience function from imutils
def dlib_to_cv_bounding_box(box):
    # convert dlib bounding box for OpenCV display
    x = box.left()
    y = box.top()
    w = box.right() - x
    h = box.bottom() - y

    return x, y, w, h


def show_detected_faces(img, bounding_boxes, facial_landmark_points):
    for face in bounding_boxes:
        # draw box for face
        x, y, w, h = dlib_to_cv_bounding_box(face)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # draw circles for landmarks
        for landmark_set in facial_landmark_points:
            for x, y in landmark_set:
                cv2.circle(img, (x, y), 1, (123, 200, 255), 5)

        # show the output image with the face detections + facial landmarks
        #cv2.imshow("Output", img)
        cv2.imwrite("saida.jpg", img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


# conversion from imutils
def landmarks_to_numpy(landmarks):
    # initialize the matrix of (x, y)-coordinates with a row for each landmark
    coords = np.zeros((len(landmarks), 2), dtype=int)

    # convert each landmark to (x, y)
    for i in range(0, len(landmarks)):
        coords[i] = (landmarks[i][0], landmarks[i][1])

    # return the array of (x, y)-coordinates
    return coords


def add_inferred_landmarks(landmark_list):
    # append extra inferred points to improve mask
    nose = landmark_list[NOSE_INDEX]
    left_ear = landmark_list[LEFT_EAR_LEFT_INDEX]
    right_ear = landmark_list[RIGHT_EAR_RIGHT_INDEX]

    # left_cheek = (left_ear.x, mouth.y)
    left_cheek = (left_ear[0], nose[1])
    right_cheek = (right_ear[0], nose[1])

    landmark_list.append(left_cheek)
    landmark_list.append(right_cheek)

def converter_haar_para_dlib(x, y, w, h):
    """
    Função para converter o formato de retângulo do Haar Cascade para o formato de retângulo do dlib.

    Args:
        retangulo_haar (list): Lista com as coordenadas [x, y, width, height].

    Returns:
        list: Lista de retângulos no formato [(x1, y1) (x2, y2)].
    """
    return [dlib.rectangle(int(x), int(y), int(x) + int(w), int(y) + int(h))]



def detect_cat_face(img):
    facial_landmark_points = []

    # pre-process the image to grayscale, a normal step for haar classifiers
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_bounding_boxes = detector(grayscale_img, 1)
    print(f"Cheguei - {DETECTOR}", face_bounding_boxes)

    if len(face_bounding_boxes) == 0:
        face_bounding_boxes = haar_detector.detectMultiScale(grayscale_img, 1.01, 3)
        print(f"Cheguei! - {HAAR_CLASSIFIER}", face_bounding_boxes, len(face_bounding_boxes))
        for (x, y, w, h) in face_bounding_boxes:
            face_bounding_boxes = converter_haar_para_dlib(x, y, w, h)


    if len(face_bounding_boxes) == 0:
        print("no cat face found in input image")
        exit(0)

    for face in face_bounding_boxes:
        landmarks = landmarks_predictor(img, face)

        landmark_list = []
        for i in range(0, landmarks.num_parts):
            landmark_list.append((landmarks.part(i).x, landmarks.part(i).y))

        add_inferred_landmarks(landmark_list)

        facial_landmark_points.append(landmarks_to_numpy(landmark_list))
        print(facial_landmark_points)

    if debug_cat_frontal_face_detection:
        show_detected_faces(img, face_bounding_boxes, facial_landmark_points)

    return face_bounding_boxes, facial_landmark_points
