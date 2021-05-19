import pandas as pd
import smtplib
import mimetypes
import os
import json
from time import sleep
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase


exel_document = pd.read_excel(r'Your path', sheet_name='namesheet', usecols=['yournamecols'])
recipients = list(set([i for i in exel_document['yournamecols']]))

#reading config file (security)
with open('config.json', 'r') as config:
    setting = json.load(config)

def send_email(recipients, message_subject, message_text, files):
    # authorization-data
    
    me = setting.get("email")
    mepass = setting.get("password")
    print(me, mepass)    

    msg = MIMEMultipart()
    msg['From'] = me
    msg['To'] = recipients
    msg['Subject'] = message_subject

    body = message_text
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    process_attachment(msg, files)
    
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(me, mepass)

    server.send_message(msg)

    server.quit()

def process_attachment(msg, files):
    for f in files:
        if os.path.isfile(f):
            attach_file(msg, f)
        elif os.path.exists(f):
            dir = os.listdir(f)
            for file in dir:
                attach_file(msg, f + '/' + file)

def attach_file(msg, filepath):
    filename = os.path.basename(filepath)
    ftype, encoding = mimetypes.guess_type(filepath)
    if ftype is None or encoding is not None:
        ftype = 'application/octet-stream'
    maintype, subtype = ftype.split('/', 1)
    if maintype == 'text':
        with open(filepath) as fp:
            file = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'image':
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    else:
        with open(filepath, 'rb') as fp:
            file= MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
            fp.close()
        encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)

files = [r'pathtodictwithfiles']

while len(recipients):
    send_email(', '.join(recipients[:30]), "Subject mail", 'Text mail', files)
    if len(recipients) >= 30:
        recipients = recipients[30:]
    else:
        recipients = []
    sleep(60) #interval between sending mails

    

