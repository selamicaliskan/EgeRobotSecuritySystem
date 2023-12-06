
import GUI_s
import trainModel_s
import faceRecognizer_s
import mailSender_s

import cv2
import time
from datetime import datetime
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import os
from PIL import ImageTk, Image, ImageGrab



class Main:

    def __init__(self):

        self.current_image = None
        self.photo = None

        self.gui_n = GUI_s.Gui_s()
        self.faceR = faceRecognizer_s.FaceRecognizer_s()
        self.trainer = trainModel_s.TrainModel_s()
        self.mailSender=mailSender_s.MailSender_s(sender_email='this.is.an.artificialintelligence@gmail.com',
                                                  sender_password='hkff dzer hkxi xrui',
                                                  subject="EGEROBOT security system!",
                                                  text="Restricted area violated! Attached is the log record and visual.",
                                                  img="image.png",
                                                  attachment="log.txt",
                                                  sent_email="selamicaliskan.ai@gmail.com")
        self.warning_flag=False
        self.time_flag = True
        self.identity="unknown"


        self.mainf()


    def mainf(self):
        """
        face recognizer ile yüzler tanınır
        opencv ile okunan anlik görüntü arayüze aktarılır
        yüzler daire biçiminde çizilip etiketlenir
        butonların aktif fonksiyonları konfigüre edilir
        """
        self.identity, x1, y1, x2, y2 = self.faceR.recognizer_s()

        self.current_image = Image.fromarray(cv2.cvtColor(self.faceR.frame, cv2.COLOR_BGR2RGB))
        self.photo = ImageTk.PhotoImage(image=self.current_image)
        self.gui_n.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.gui_n.root.after(10, self.mainf)

        self.gui_n.drawFaces(self.identity, x1, y1, x2, y2)
        if self.gui_n.addPersonFlag:
            self.gui_n.addPersonBtn.config(command=lambda: self.new_person(self.current_image))
        if self.gui_n.trainFlag:
            self.gui_n.trainBtn.config(command=self.trainer.train_all_database)
        if self.gui_n.restrict_flag:
            self.gui_n.restrictedBtn.config(command=self.restricted_control(self.identity, x1, y1, x2, y2))


    def new_person(self, cur_img):
        """
        yeni kisi ekleme butonu aktif fonksiyonu
        :param cur_img: anlik yakalanan goruntu
        """
        if cur_img is not None:
            name = self.gui_n.person_name_txt.get(1.0, "end-1c")
            if name == '':
                messagebox.showwarning("Person name is empty!", "Please enter the person name.")
            else:
                p = 'photos/' + str(name) + '.jpg'
                file_path = os.path.expanduser(p)
                cur_img.save(file_path)




    def restricted_control(self, identity, x1, y1, x2, y2): # btn3 actin
        """
        yasakli bolge kontrolu aktif fonksiyonu
        yasakli bolgeler kontrol edilir, ihlal varsa kirmizi yoksa yesil olarak bolge cizilir
        :param identity: pasif durumda
        :param x1: x1 koordinati
        :param y1: y1 koordinati
        :param x2: x2 koordinati
        :param y2: y2 koordinati
        """
        self.logging_mail()
        if len(self.gui_n.coorList) > 1:
            center_x = x1 + (x2 - x1) / 2
            center_y = y1 + (y2 - y1) / 2
            if (center_x > self.gui_n.coorList[0][0] and center_y > self.gui_n.coorList[0][1] and center_x < self.gui_n.coorList[1][0] and center_y < self.gui_n.coorList[1][1]):
                self.gui_n.create_rectangle(self.gui_n.coorList[0][0], self.gui_n.coorList[0][1],
                                      self.gui_n.coorList[1][0], self.gui_n.coorList[1][1],
                                      alpha=0.3, fill='red')

                self.warning_flag=True

            else:
                self.gui_n.create_rectangle(self.gui_n.coorList[0][0], self.gui_n.coorList[0][1],
                                      self.gui_n.coorList[1][0], self.gui_n.coorList[1][1],
                                      alpha=0.3, fill='green')
                self.warning_flag=False


    def logging_mail(self):
        """
        yasakli bolge aktif oldugu durumda:
            her 10 saniyede bir loglama yapılır
            her 10 saniyede bir yasakli bolge kontrol edilir
            yasakli bolge ihlali olması durumunda log kaydi ve ihlal fotografi mail ile gonderilir
        """
        cur_time = time.time()
        seconds = int(cur_time % 60)

        if seconds % 10 == 0 and self.time_flag:

            date_and_time = datetime.now()
            formatted_time = date_and_time.strftime('%Y-%m-%d %H:%M:%S')
            f = open("log.txt", "a")
            time.sleep(1)

            if self.warning_flag:

                print('{} {} is in the restricted area!'.format(formatted_time, self.identity.capitalize()))
                f.write('{} {} is in the restricted area!\n'.format(formatted_time, self.identity.capitalize()))

                self.getCanvasImage(self.gui_n.canvas)
                f.close()
                self.mailSender.send_mail()

            else:
                print('{} There is no one in the restricted area.'.format(formatted_time))
                f.write('{} There is no one in the restricted area.\n'.format(formatted_time))
                f.close()

            self.time_flag = False
        elif seconds % 10 == 1:
            self.time_flag = True


    def getCanvasImage(self,widget):
        """
        arayuz uzerinden goruntu yakalamak
        :param widget:
        """
        xr = self.gui_n.root.winfo_rootx() + widget.winfo_x()
        yr = self.gui_n.root.winfo_rooty() + widget.winfo_y()
        x1r = m.gui_n.x + widget.winfo_width()
        y1r = m.gui_n.y + widget.winfo_height()
        ImageGrab.grab().crop((xr, yr, x1r, y1r)).save("image.png")



if __name__=="__main__":

    m=Main()
    m.gui_n.root.bind('<Button 1>', m.gui_n.callback)
    # m.mainf()

    m.gui_n.root.mainloop()








