
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image

import trainModel_s




class Gui_s:

    def __init__(self):
        self.trainFlag = False
        self.addPersonFlag = False
        self.root = tk.Tk()
        self.root.title("EGEROBOT SECURITY SYSTEM")
        self.trainer = trainModel_s.TrainModel_s()

        self.icon = Image.open('egerobot_logo.jpeg')
        self.photo = ImageTk.PhotoImage(self.icon)
        self.root.wm_iconphoto(False, self.photo)






        self.canvas = tk.Canvas(self.root, width=1080, height=720, bd=5, bg='#000000')

        self.addPersonBtn = tk.Button(self.root, text="Add New Person", command= self.new_person_action, border=0)
        self.trainBtn = tk.Button(self.root, text="Train Dataset", command=self.train_all_database_action, border=0)
        self.restrictedBtn = tk.Button(self.root, text="btn3", command=self.restricted_control_action, border=0)

        self.person_name_txt = tk.Text(self.root, width=20, height=1)

        self.person_label = tk.Label(self.root, text='Enter Person Name:')

        self.add_person_btn_img = PhotoImage(file="ad_person_img.png")
        self.add_person_btn_img = self.add_person_btn_img.subsample(2, 2)
        self.train_btn_img = PhotoImage(file="train_model_img.png")
        self.train_btn_img = self.train_btn_img.subsample(2, 2)
        self.restrictedAreaBtn_img = PhotoImage(file="restricted_img.png")
        self.restrictedAreaBtn_img = self.restrictedAreaBtn_img.subsample(x=2, y=2)

        self.add_person_btn_green_img = PhotoImage(file="addPersonOnClick.png")
        self.add_person_btn_green_img = self.add_person_btn_green_img.subsample(2, 2)
        self.train_btn_green_img = PhotoImage(file="trainAIOnClick.png")
        self.train_btn_green_img = self.train_btn_green_img.subsample(2, 2)
        self.restrictedAreaBtn_green_img = PhotoImage(file="restrictedOnClick.png")
        self.restrictedAreaBtn_green_img = self.restrictedAreaBtn_green_img.subsample(x=2, y=2)

        self.egerobotLogo = Image.open("egerobot_logo.jpeg")
        self.egerobotLogo = self.egerobotLogo.resize((150, 150))
        self.egerobotLogo = ImageTk.PhotoImage(self.egerobotLogo)
        self.egerobotLabel = tk.Label(image=self.egerobotLogo)

        # Placements
        self.canvas.grid(row=0, column=0, rowspan=7)
        self.addPersonBtn.grid(row=2, column=1, padx=10, pady=0, sticky=tk.W)
        self.trainBtn.grid(row=4, column=1, padx=10, pady=0, sticky=tk.W)
        self.restrictedBtn.grid(row=5, column=1, padx=10, pady=0, sticky=tk.W)
        self.person_name_txt.grid(row=1, column=1, padx=10)
        self.person_label.grid(row=0, column=1, padx=10, pady=0)




        self.addPersonBtn.config(image=self.add_person_btn_img)




        self.trainBtn.config(image=self.train_btn_img)

        self.restrictedBtn.config(image=self.restrictedAreaBtn_img)
        self.egerobotLabel.grid(row=6, column=1, padx=10, pady=0)

        self.images = []
        self.coorList = []
        self.restrict_flag=False
        self.x=None
        self.y=None


    def new_person_action(self):
        """
        yeni kisi ekleme butonu gecici fonksiyonudur.
        """
        self.addPersonBtn.config(image=self.add_person_btn_green_img)
        self.addPersonFlag=True

    #
    def restricted_control_action(self):
        """
        yasakli bölge ekleme butonu gecici fonksiyonudur.
        """
        self.restrictedBtn.config(image=self.restrictedAreaBtn_green_img)
        self.restrict_flag=True


    #
    def train_all_database_action(self):
        """
        veri tabanindaki tüm verilerin egitim butonunun gecici fonskiyonudur.
        """
        self.trainBtn.config(image=self.train_btn_green_img)
        self.trainFlag=True







    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        """
        tkinter.canvas.create_rectangle fonskiyonuna alpha parameteresi eklemek için yazilmis bir fonksiyondur.
        :param x1: x1 koordinati
        :param y1: y1 kooridnati
        :param x2: x2 koordinati
        :param y2: y2 koordinati
        :param kwargs: parametre list
        """
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)





    def drawFaces(self, identity, x1, y1, x2, y2):
        """
        Tespit edilen yüzlerin etrafına daire cizip icerisine isim yazma
        :param identity: kimlik bilgisi
        :param x1: x1 koordinati
        :param y1: y1 koordinati
        :param x2: x2 koordinati
        :param y2: y2 koordinati
        """
        self.canvas.create_oval(x1, y1, x2, y2, width=5, outline='blue')
        center_x = x1 + (x2 - x1) / 2
        center_y = y1 + (y2 - y1) / 2
        self.canvas.create_text(center_x, center_y, text=identity.capitalize(), fill='blue',
                                font=("Purisa", 20, 'bold'))

    def callback(self, eventorigin):
        """
        mouse tiklama koordinatlarını bir listede toplar
        :param eventorigin: mouse koordinat bilgisi nesnesi
        """
        if self.restrict_flag:
            self.x = eventorigin.x
            self.y = eventorigin.y
            if self.x > 0 and self.x < 1080 and self.y > 0 and self.y < 720:
                self.coorList.append([self.x, self.y])

