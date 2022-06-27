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
    def send(self, incident):
        if incident.status == 'Recovered':
            return

        payload = SquadCast.__payload.copy()
        payload['message'] = str(incident)
        payload['description'] = incident.description
        requests.post(SquadCast.__endpoint % self.token, json=payload)
