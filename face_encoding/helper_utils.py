import logging

import dlib
import cv2
import face_recognition
import numpy as np

face_detector = dlib.get_frontal_face_detector()

predictor_model = 'models/shape_predictor_68_face_landmarks.dat'
pose_predictor = dlib.shape_predictor(predictor_model)

face_recognition_model = 'models/dlib_face_recognition_resnet_model_v1.dat'
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)


def load_image_file(image, mode='RGB'):
    img = image
    if img.shape[0] > 800:
        baseheight = 500
        w = (baseheight / img.shape[0])
        p = int(img.shape[1] * w)
        img = cv2.resize(img, (baseheight, p))
    elif img.shape[1] > 800:
        baseheight = 500
        w = (baseheight / img.shape[1])
        p = int(img.shape[0] * w)
        img = cv2.resize(img, (p, baseheight))

    return img


def _tuple_to_rect(rect):
    return dlib.rectangle(rect[3], rect[0], rect[1], rect[2])


def _raw_face_locations(img, number_of_times_to_upsample=1):
    return face_detector(img, number_of_times_to_upsample)


def _raw_face_landmarks(face_image, face_locations=None):
    if face_locations is None:
        face_locations = _raw_face_locations(face_image)
    else:
        face_locations = [_tuple_to_rect(face_location) for face_location in face_locations]

    return [pose_predictor(face_image, face_location) for face_location in face_locations]


def face_encodings(face_image, known_face_locations=None, num_jitters=1):
    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations)

    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]

def get_encoding(image):
    try:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        return encode.tolist()
    except Exception as e:
        print(e)
        return None
