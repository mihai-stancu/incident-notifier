import os
import yaml

from Incident import Incident
from Handlers import Handler

with open(os.path.dirname(__file__) + '/../etc/handlers.yml') as fh:
    handlers = yaml.safe_load(fh)

for key, config in handlers.items():
    handler = Handler.create(config['type'], config['params'])
    for project in config['projects']:
        Incident.register(project, key, handler)
