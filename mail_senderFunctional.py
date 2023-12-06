
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os

def send_mail():

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()

    smtp.login('this.is.an.artificialintelligence@gmail.com', 'hkff dzer hkxi xrui')

    def message(subject="Python Notification",
                text="", img=None,
                attachment=None):
        msg = MIMEMultipart()

        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        if img is not None:

            if type(img) is not list:
                img = [img]

            for one_img in img:
                img_data = open(one_img, 'rb').read()

                msg.attach(MIMEImage(img_data,
                                     name=os.path.basename(one_img)))

        if attachment is not None:

            if type(attachment) is not list:

                attachment = [attachment]

            for one_attachment in attachment:
                with open(one_attachment, 'rb') as f:

                    file = MIMEApplication(
                        f.read(),
                        name=os.path.basename(one_attachment)
                    )
                file['Content-Disposition'] = f'attachment;\ filename = "{os.path.basename(one_attachment)}"'

                msg.attach(file)
        return msg

    msg = message("EGEROBOT security system!", "Restricted area violated! Attached is the log record and visual.",
                  r"image.png",
                  r"demoLog1.txt")

    to = ["selamicaliskan.ai@gmail.com"]

    smtp.sendmail(from_addr="this.is.an.artificialintelligence@gmail.com",
                  to_addrs=to, msg=msg.as_string())

    smtp.quit()
