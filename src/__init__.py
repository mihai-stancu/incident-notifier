import os
import yaml

from Incident import Incident

with open(os.path.dirname(__file__) + '/../etc/projects.yml') as fh:
    config = yaml.safe_load(fh)

for project, handlers in config.items():
    Incident.register(project, handlers)
