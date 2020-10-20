import os
import yaml

path = os.path.dirname(os.path.abspath(__file__))

if os.path.isfile(path + '/config.yml'):
    with open(path + "/config.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
else:
    exit()
