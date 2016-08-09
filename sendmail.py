#!/usr/bin/python

import smtplib,sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

v = sys.argv[1].split('/')
filename=v[len(v)-1]


SUBJECT = "Email Data"
EMAIL_FROM='pi4@free.fr'
EMAIL_TO='arnaud.vial@free.fr'

msg = MIMEMultipart()
msg['Subject'] = SUBJECT 
msg['From'] = EMAIL_FROM
msg['To'] = ''.join(EMAIL_TO)

part = MIMEBase('application', "octet-stream")
part.set_payload(open(sys.argv[1], "rb").read())
Encoders.encode_base64(part)

part.add_header('Content-Disposition', 'attachment; filename="'+filename+'"')

msg.attach(part)

server = smtplib.SMTP('smtp.free.fr')
server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
server.close()
