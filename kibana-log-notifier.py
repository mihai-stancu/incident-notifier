#!/usr/bin/python3

import json
import os
import smtplib
import sys

smtp_host = os.getenv('MAIL_HOST')
smtp_port = os.getenv('MAIL_PORT')
smtp_user = os.getenv('MAIL_USER')
smtp_pass = os.getenv('MAIL_PASS')
recipients = os.getenv('MAIL_TO').split(',')
subject = os.getenv('MAIL_SUBJECT')
sender_address = os.getenv('MAIL_USER')

def sendMail(TEXT):
    """this is some test documentation in the function"""
    message = """\
From: %s
To: %s
Subject: %s

%s
""" % (sender_address, ", ".join(recipients), subject, TEXT)
    # Send the mail
    smtp = smtplib.SMTP(smtp_host, smtp_port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(smtp_user, smtp_pass)
    smtp.sendmail(smtp_user, recipients, message)
    smtp.quit()


for line in sys.stdin:
    record = json.loads(line)
    if record["type"] == "log" and "error" in record["tags"]:
        sendMail(record["message"])
