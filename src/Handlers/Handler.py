class Handler:
    __types = {}
    __handlers = {}

    @staticmethod
    def register(type, constructor):
        Handler.__types[type] = constructor
        return Handler

    @staticmethod
    def create(name, type, args):
        constructor = Handler.__types[type]
        Handler.__handlers[name] = constructor(**args)
        return Handler

    @staticmethod
    def find(name):
        return Handler.__handlers[name]

    def send(self, incident):
        pass
