
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os


class MailSender_s:
    def __init__(self,sender_email, sender_password, subject, text, img, attachment, sent_email):
        self.sender_email=sender_email
        self.sender_password=sender_password
        self.subject=subject
        self.text=text
        self.img=img
        self.attachment=attachment
        self.sent_email=sent_email
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)

    def message(self,subject="Python Notification",text="", img=None, attachment=None):

        """
        Sunucuya gönderilecek mesaj nesnesi içeriği
        :param subject: Konu
        :param text: okunacak metin
        :param img: okunacak resim
        :param attachment: okunacak dosya
        :return: msg
        """

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg.attach(MIMEText(text))

        if img is not None:
            if type(img) is not list:
                img = [img]
            for one_img in img:
                img_data = open(one_img, 'rb').read()
                msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))

        if attachment is not None:
            if type(attachment) is not list:
                attachment = [attachment]
            for one_attachment in attachment:
                with open(one_attachment, 'rb') as f:
                    file = MIMEApplication(
                        f.read(),
                        name=os.path.basename(one_attachment))
                file['Content-Disposition'] = f'attachment;\ filename = "{os.path.basename(one_attachment)}"'
                msg.attach(file)
        return msg

    def send_mail(self):
        """
        Sunucuya bağlanıp bail gönderme
        """
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(self.sender_email,self.sender_password)
        msg=self.message(self.subject,self.text,self.img,self.attachment)
        to=[self.sent_email]
        self.smtp.sendmail(from_addr=self.sender_email,
                      to_addrs=to, msg=msg.as_string())
        self.smtp.quit()
        self.smtp.close()





