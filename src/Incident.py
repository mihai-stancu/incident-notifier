import json

from datetime import datetime
from Handlers import Handler

class Incident:
    __statuses = {
        'alert': 'alert',
        'recovered': 'recovered',
        'Alert': 'alert',
        'Fired': 'alert',
        'Uptime Down Monitor': 'alert',
        'Recovered': 'recovered',
    }

    __handlers = {}

    @staticmethod
    def register(project, handlers):
        Incident.__handlers[project] = handlers
        return Incident

    def __init__(self, line):
        raw = json.loads(line)
        raw = {k: (v if v is not None else '') for k, v in raw.items()}

        self.id = raw['id']
        self.server = raw['server'] or '-'.join(raw['id'].replace('_', '-').split('-')[:4])
        self.project = "-".join(self.server.split('-')[:2])
        self.rule = raw['rule']
        self.status = Incident.__statuses[raw['status']] if raw['status'] in Incident.__statuses else 'alert'
        if raw['timestamp']:
            self.timestamp = datetime.strptime(raw['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.timestamp = datetime.now()
        self.description = raw['description']

    def format(self, format = ''):
        return format.format(
            id = self.id,

            project = self.project,
            server = self.server,

            rule = self.rule,
            status = self.status,

            timestamp = self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            date = self.timestamp.strftime('%Y-%m-%d'),
            time = self.timestamp.strftime('%H:%M:%S'),

            description = self.description,
         )

    def handle(self):
        handlers = self.__handlers['default']
        if self.project in self.__handlers:
            handlers = self.__handlers[self.project]

        for handler in handlers:
            try:
                Handler.find(handler).send(self)
                self.log("was handled", handler)
            except Exception as ex:
                self.log("had an exception")
                print(ex)

    def log(self, prefix, handler = None):
        incident = self.format('{server} {rule} {status} {timestamp}')
        msg = '{incident} {prefix}'.format(incident = incident, prefix = prefix)
        if handler is not None:
            msg += ' via ' + handler
        print(msg)
