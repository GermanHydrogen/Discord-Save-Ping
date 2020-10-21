import os
import yaml

path = os.path.dirname(os.path.abspath(__file__))

if os.path.isfile(path + '/config.yml'):
    with open(path + "/config.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
else:
    exit()

if os.path.isfile(path + '/pingPair.yml'):
    with open(path + "/pingPair.yml", 'r') as ymlfile:
        pingPair = yaml.safe_load(ymlfile)
else:
    pingPair = {}

if os.path.isfile(path + '/moderator.yml'):
    with open(path + "/moderator.yml", 'r') as ymlfile:
        moderatorRoles = yaml.safe_load(ymlfile)
else:
    moderatorRoles = {}
