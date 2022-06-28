import os
import smtplib

from .Handler import Handler

#
# Send email via SMTP
#
class Mail(Handler):
    __template = (
        "To: {recipients}\n"
        "From: {sender}\n"
        "Subject: {subject}\n"
        "\n"
        "{body}"
    )

    def __init__(self, host, port, user, cred, recipients, sender = None, title_format = None, content_format = None):
        self.host = host
        self.port = port

        self.user = user
        self.cred = cred

        self.recipients = recipients
        self.sender = sender or ('"%s" <%s>' % (os.getenv('MAIL_DEFAULT_SENDER'), self.user))

        self.title_format = title_format or '{server} {rule} {status} {timestamp}'
        self.content_format = content_format or '{description}'

    def send(self, incident):
        if incident.status == 'recovered':
            return

        body = self.__template.format(
            recipients = ', '.join(self.recipients),
            sender = self.sender,
            subject = incident.format(self.title_format),
            body = incident.format(self.content_format),
        )

        smtp = smtplib.SMTP(self.host, self.port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.user, self.cred)
        smtp.sendmail(self.user, self.recipients, body)
        smtp.quit()
