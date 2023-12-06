
import cv2
import os
import numpy as np
import pickle
from keras_facenet import FaceNet
import faceDetector_s



class TrainModel_s:

    def __init__(self):
        self.data_path='photos/'
        self.database = {}
        self.MyFaceNet = FaceNet()
        self.cimage=None
        self.faceDetector = faceDetector_s.FaceDetector_s(self.cimage)

    def train_all_database(self):
        """
        fotograf verilerini okur
        yuzleri tespit eder
        ozellik vektorlerini cikarir
        veri tabanına kaydeder
        """
        for filename in os.listdir(self.data_path):
            path = self.data_path + filename
            gbr1 = cv2.imread(path)
            # face = self.detect_faces(gbr1)
            face=self.faceDetector.detect_faces(gbr1)

            face = np.expand_dims(face, axis=0)
            signature = self.MyFaceNet.embeddings(face)
            self.database[os.path.splitext(filename)[0]] = signature
        # 2

        myFile = open('data.pkl', 'wb')
        pickle.dump(self.database, myFile)
        myFile.close()
        print(self.database)
        # self.gui_ne.trainBtn.config(image=self.gui_ne.train_btn_img)
        # self.gui_ne.trainFlag=False