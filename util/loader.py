import os
import yaml

path = os.path.abspath(os.curdir)

if os.path.isfile(path + '/configuration/config.yml'):
    with open(path + "/configuration/config.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
else:
    exit()


if os.path.isfile(path + '/configuration/pingPair.yml'):
    with open(path + "/configuration/pingPair.yml", 'r') as ymlfile:
        pingPair = yaml.safe_load(ymlfile)
else:
    pingPair = {}

if os.path.isfile(path + '/configuration/moderator.yml'):
    with open(path + "/configuration/moderator.yml", 'r') as ymlfile:
        moderatorRoles = yaml.safe_load(ymlfile)
else:
    moderatorRoles = {}
