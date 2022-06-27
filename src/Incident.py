import json
import yaml

from datetime import datetime
from Handlers import Handler

class Incident:
    __handlers = {}

    @staticmethod
    def register(project, handlers):
        Incident.__handlers[project] = handlers
        return Incident

    def __init__(self, line):
        record = json.loads(line)

        raw = yaml.safe_load(record['message'].replace(';', "\n"))
        raw = {k: (v if v is not None else '') for k, v in raw.items()}

        self.server = raw['server'] or raw['id']
        self.rule = raw['rule']
        self.status = raw['status']
        self.timestamp = raw['timestamp'] or datetime.now()
        self.description = raw['description']
        self.project = "-".join(self.server.split('-')[:2])

    def id(self):
        return "%s.%s.%s" % (self.timestamp.strftime('%Y%m%d%H%M%S'), self.server, self.rule)

    def __str__(self):
        return " ".join([self.timestamp.strftime('%Y-%m-%d %H:%M:%S'), self.server, self.rule, self.status])

    def handle(self):
        if not self.project in self.__handlers:
            self.log("is unhandled")
            return

        for handler in self.__handlers[self.project]:
            try:
                Handler.find(handler).send(self)
                self.log("was handled", handler)
            except Exception as ex:
                self.log("had an exception")
                print(ex)

    def log(self, prefix, handler = None):
        if handler is not None:
            print("%s %s via %s" % (self, prefix, handler))
        else:
            print("%s %s" % (self, prefix))
