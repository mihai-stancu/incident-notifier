#!/usr/bin/python3
import docker
import json
import os
import smtplib

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

client = docker.from_env()
container = client.containers.get('kib01')

for line in container.logs(stream=True, tail=10):
    record = json.loads(line)
    if record["type"] == "log" and "error" in record["tags"]:
        sendMail(record["message"])
