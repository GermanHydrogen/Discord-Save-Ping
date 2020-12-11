import os
import yaml
import codecs

path = os.path.abspath(os.curdir)

if os.path.isfile(path + '/configuration/config.yml'):
    with open(path + "/configuration/config.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
else:
    exit()


if os.path.isfile(path + '/configuration/pingPair.yml'):
    with codecs.open(path + "/configuration/pingPair.yml", 'r', "utf-8") as ymlfile:
        pingPair = yaml.safe_load(ymlfile)
else:
    pingPair = {}

if os.path.isfile(path + '/configuration/moderator.yml'):
    with codecs.open(path + "/configuration/moderator.yml", 'r', "utf-8") as ymlfile:
        guildRoles = yaml.safe_load(ymlfile)
else:
    guildRoles = {}
