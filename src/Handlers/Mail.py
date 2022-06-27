import smtplib

from .Handler import Handler

#
# Send email via SMTP
#
class Mail(Handler):
    __template = (
        "From: %s\n"
        "Subject: %s\n"
        "%s"
    )

    def __init__(self, host, port, user, cred, to):
        self.host = host
        self.port = port

        self.user = user
        self.cred = cred

        self.to = to

    def send(self, incident):
        if incident.status == 'Recovered':
            return

        smtp = smtplib.SMTP(self.host, self.port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.user, self.cred)
        smtp.sendmail(self.user, self.to, self.__template % (self.user, incident, incident.description))
        smtp.quit()

    def set_recipients(self, recipients):
        self.to = recipients
        return self