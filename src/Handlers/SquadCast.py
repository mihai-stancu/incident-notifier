import requests

from .Handler import Handler

class SquadCast(Handler):
    __endpoint = "https://api.squadcast.com/v2/incidents/api/%s"
    __payload = {"message": None, "description": None, "status": "trigger"}

    def __init__(self, token):
        self.token = token

    #
    # WebHook trigger
    #
    def send(self, message, description, tags):
        payload = SquadCast.__payload.copy()
        payload['message'] = message
        payload['description'] = description
        requests.post(SquadCast.__endpoint % self.token, json=payload)
