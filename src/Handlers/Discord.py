import requests

from .Handler import Handler

class Discord(Handler):
    __endpoint = "https://discord.com/api/webhooks/%s/%s"
    __payload = {"content": None}

    def __init__(self, channel, token, title_format = None, content_format = None):
        self.channel = channel
        self.token = token
        self.title_format = title_format or ':warning: **{server} {rule} {status}** {timestamp}'
        self.content_format = content_format or '*{description}*'

    #
    # WebHook trigger
    #
    def send(self, incident):
        if incident.status == 'recovered':
            return

        payload = Discord.__payload.copy()
        payload['content'] = incident.format(self.title_format) + "\n" + incident.format(self.content_format)
        requests.post(Discord.__endpoint % (self.channel, self.token), json=payload)
