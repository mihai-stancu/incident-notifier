class Handler:
    __types = {}

    @staticmethod
    def register(type, constructor):
        Handler.__types[type] = constructor
        return Handler

    @staticmethod
    def create(type, args):
        constructor = Handler.__types[type]
        return constructor(**args)

    def send(self, incident):
        pass
