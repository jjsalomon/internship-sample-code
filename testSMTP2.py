# -*- coding: utf-8 -*-

import smtplib


CONTENT =  "\n Hello Rakesh, Test Email"
EMAIL_HOST = "mailo2.uhc.com"
EMAIL_PORT = 25

TO = "rakesh_sudhakar@optum.com"
FROM = "parkinsontracker@optum.com"

server = smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
server.sendmail(FROM,TO,CONTENT)
server.quit()