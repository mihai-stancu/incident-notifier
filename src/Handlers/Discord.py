import requests

from .Handler import Handler

class Discord(Handler):
    __endpoint = "https://discord.com/api/webhooks/%s/%s"
    __payload = {"content": None}

    def __init__(self, channel, token):
        self.channel = channel
        self.token = token

    #
    # WebHook trigger
    #
    def send(self, incident):
        if incident.status == 'Recovered':
            return

        payload = Discord.__payload.copy()
        payload['content'] = '**' + str(incident) + '**' + "\n" + incident.description
        print(Discord.__endpoint % (self.channel, self.token), requests.post(Discord.__endpoint % (self.channel, self.token), json=payload))
