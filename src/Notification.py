import sys
import json

import json

class Notification:
    __MARKER = "kibana-log-notifier"

    __handlers = {}

    @staticmethod
    def register(project, type, handler):
        if project not in Notification.__handlers:
            Notification.__handlers[project] = {}
        Notification.__handlers[project][type] = handler
        return Notification

    def __init__(self, line):
        record = json.loads(line)
        raw = record['message'].split(";")
        self.message = raw[0].replace('Server log: ', '')
        self.tags = raw[1].replace('Tags: ', '').split(',')
        self.description = "\n".join(raw[2:])
        self.project = "-".join(self.message.split(' ')[0].split('-')[0:2])

    def handle(self):
        if Notification.__MARKER not in self.tags:
            return

        if self.project not in self.__handlers:
            return

        for type in self.__handlers[self.project]:
            self.__handlers[self.project][type].send(self.message, self.description, self.tags)
