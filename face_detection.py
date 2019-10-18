import math
import numpy as np
from mtcnn.mtcnn import MTCNN
import tensorflow.keras as keras
import cv2
import pickle
from sklearn.preprocessing import Normalizer
from prepare_training_embeddings_data import get_embedding

detector = MTCNN()
keras_model = keras.models.load_model("./model/facenet_keras.h5")
svc_model = pickle.load(open("./data/syna_svc.model", "rb"))


def predict_face(face):
    face = cv2.resize(face, (160, 160), interpolation=cv2.INTER_AREA)
    face = np.asarray(face)

    face_embedding = get_embedding(keras_model, face)
    in_encoder = Normalizer(norm="l2")
    face_embedding = np.expand_dims(face_embedding, axis=0)
    face_embedding = in_encoder.transform(face_embedding)
    result = svc_model.predict(face_embedding)
    print("!!!!!!!!!!!!!!", result)

    return result[0]


def test_static_img():
    #inputImg = cv2.imread("./test_image/lfw/George_W_Bush/George_W_Bush_0003.jpg")
    inputImg = cv2.imread(r"E:/deeplearning/test_image/tom2.jpg")
    inputImg = cv2.cvtColor(inputImg, cv2.COLOR_RGB2BGR)
    faces = detector.detect_faces(inputImg)

    if len(faces) >= 1:
        for i in range(len(faces)):
            x1, y1, width, height = faces[i]['box']
            x2 = x1 + width
            y2 = y1 + height
            cv2.rectangle(inputImg, (x1, y1), (x2, y2), (0, 255, 0), 2)

            face = inputImg[y1: y1 + height, x1:x1 + width]
            #predict
            predict = predict_face(face)

            cv2.putText(inputImg, "face" + str(predict), (x1, y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 0, 255), 1)

    inputImg = cv2.cvtColor(inputImg, cv2.COLOR_RGB2BGR)

    cv2.imshow("camera", inputImg)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_live_cam():
    capture = cv2.VideoCapture(0)
    cv2.namedWindow("camera", 1)

    while True:
        ret, inputImg = capture.read()
        inputImg = cv2.cvtColor(inputImg, cv2.COLOR_BGR2RGB)
        #x,y,z = inputImg.shape
        #x_scaled = (int)(x / 10)
        #y_scaled = (int)(y / 10)
        #inputImg = cv2.resize(inputImg, (y_scaled, x_scaled), interpolation=cv2.INTER_AREA)

        faces = detector.detect_faces(inputImg)
        #[{
        #  'box': [277, 90, 48, 63],
        #  'keypoints': {'nose': (303, 131), 'mouth_right': (313, 141), 'right_eye': (314, 114), 'left_eye': (291, 117), 'mouth_left': (296, 143)},
        #  'confidence': 0.99851983785629272
        #  }]
        if len(faces) >= 1:
            for i in range(len(faces)):
                x1, y1, width, height = faces[i]['box']
                x1 = abs(x1)
                y1 = abs(y1)
                x2 = x1 + width
                y2 = y1 + height
                cv2.rectangle(inputImg, (x1, y1), (x2, y2), (0, 255, 0), 2)
                face = inputImg[y1: y1 + height, x1:x1 + width]
                # predict
                predict = predict_face(face)
                cv2.putText(inputImg, "face" + str(predict), (x1, y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 0, 255), 1)

        inputImg = cv2.cvtColor(inputImg, cv2.COLOR_RGB2BGR)
        cv2.imshow("camera", inputImg)
        key = cv2.waitKey(1)
        if key == 27:   # key = Esc
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    #test_static_img()
    test_live_cam()


