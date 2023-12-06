

from keras_facenet import FaceNet
import cv2
import numpy as np
import pickle
import faceDetector_s



class FaceRecognizer_s:

    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.identity=None
        self.x1, self.y1, self.x2,self.y2=None, None, None, None
        self.MyFaceNet = FaceNet()
        self.frame=None
        self.faceDetector=faceDetector_s.FaceDetector_s(self.frame)


    def read_database(self,filename):
        """
        veri tabanını okur.
        :param filename: veri tabanı dosya yolu
        :return: database (type:dict)
        """
        myFile = open(filename, 'rb')
        database = pickle.load(myFile)
        myFile.close()
        return database

    def read_camera(self):
        """
        kamerayı okur.
        :return: return(boolean) ifadesi ve frame anlik yakalanan goruntu
        """
        ret,frame=self.video_capture.read()
        return ret,frame



    def recognizer_s(self):

        """
        kamerayı okur.
        face detector ile yüzleri tespit eder.
        özellik vektörü elde eder.
        veritabanındaki vektörler ile karşılaştırıp identity atar
        koordinatlar dahil return eder
        returns: x1, y1, x2, y2, identity
        """

        database=self.read_database('data.pkl')

        ret,self.frame=self.read_camera()
        if ret:
            face, self.x1, self.y1, self.x2, self.y2=self.faceDetector.detect_faces(self.frame,coor=True)
            face = np.expand_dims(face, axis=0)
            signature = self.MyFaceNet.embeddings(face)

            min_dist = 100
            self.identity = ' '
            for key, value in database.items():
                dist = np.linalg.norm(value - signature)
                if dist < min_dist:
                    min_dist = dist

                    self.identity = key
                if min_dist>1:
                    self.identity="unknown"

            return self.identity, self.x1, self.y1, self.x2, self.y2
        

# if __name__=="__main__":
#     fr=FaceRecognizer_s()
#     fr.recognizer_s()