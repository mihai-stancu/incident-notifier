import requests

from .Handler import Handler

class SquadCast(Handler):
    __endpoint = "https://api.squadcast.com/v2/incidents/api/{token}"
    __payload = {"message": None, "description": None, "status": "trigger"}

    def __init__(self, token, title_format = None, content_format = None):
        self.token = token
        self.title_format = title_format or '{server} {rule} {timestamp}'
        self.content_format = content_format or '{description}'

    #
    # WebHook trigger
    #
    def send(self, incident):
        payload = SquadCast.__payload.copy()
        if incident.status == 'recovered':
            payload['status'] = 'resolve'

        payload['event_id'] = incident.format('{date}.{server}.{rule}')
        payload['message'] = incident.format(self.title_format)
        payload['description'] = incident.format(self.content_format)
        requests.post(SquadCast.__endpoint.format(token = self.token), json=payload)
