import json
import yaml

class Incident:
    __handlers = {}

    @staticmethod
    def register(project, key, handler):
        if project not in Incident.__handlers:
            Incident.__handlers[project] = {}
        Incident.__handlers[project][key] = handler
        return Incident

    def __init__(self, line):
        record = json.loads(line)

        raw = yaml.safe_load(record['message'].replace(';', "\n"))

        self.server = raw['server']
        self.rule = raw['rule']
        self.status = raw['status']
        self.timestamp = raw['timestamp'].strftime('%Y-%m-%d %H:%M:%S %z')
        self.description = raw['description']
        self.project = "-".join(self.server.split('-')[:2])

    def __str__(self):
        return " ".join([self.timestamp, self.server, self.rule, self.status])

    def handle(self):
        if not self.project in self.__handlers:
            self.log("is unhandled")
            return

        for key, handler in self.__handlers[self.project].items():
            try:
                handler.send(self)
                self.log("was handled", key)
            except Exception as ex:
                self.log("had an exception")
                print(ex)

    def log(self, prefix, handler = None):
        if handler is not None:
            print("%s %s via %s" % (self, prefix, handler))
        else:
            print("%s %s" % (self, prefix))
