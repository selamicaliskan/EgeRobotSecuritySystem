
from PIL import Image
import cv2
import numpy as np


class FaceDetector_s:
    def __init__(self,cframe):
        self.cframe=cframe
        self.HaarCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def detect_faces(self,cframe,coor=False):
        """

        :param cframe: current frame (anlik olarak gonderilen goruntude yuz tespiti yapar.)
        :param coor: (boolean) sadece yuz fotografini almak istersek False, koordinatlari da almak istersek True
        :return:
        """
        faces = self.HaarCascade.detectMultiScale(cframe, 1.1, 4)


        if len(faces) > 0:
            x1, y1, w, h = faces[0]
        else:
            x1, y1, w, h = 1, 1, 1, 1

        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + w, y1 + h
        img = cv2.cvtColor(cframe, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img_array = np.asarray(img)

        face = img_array[y1:y2, x1:x2]

        face = Image.fromarray(face)
        face = face.resize((160, 160))
        face = np.asarray(face)

        if coor:
            return face, x1, y1, x2, y2
        else:
            return face