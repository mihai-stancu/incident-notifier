import os
import yaml

from .Discord import Discord
from .Handler import Handler
from .Mail import Mail
from .SquadCast import SquadCast

Handler.register("discord", Discord)
Handler.register("mail", Mail)
Handler.register("squadcast", SquadCast)

with open(os.path.dirname(__file__) + '/../../etc/handlers.yml') as fh:
    config = yaml.safe_load(fh)

for name, config in config.items():
    Handler.create(name, config['type'], config['params'])
