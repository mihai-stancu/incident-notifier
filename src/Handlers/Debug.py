from pprint import pp;

from .Handler import Handler

class Debug(Handler):
    #
    # Print to output
    #
    def send(self, incident):
        pp(vars(incident), indent=2)
