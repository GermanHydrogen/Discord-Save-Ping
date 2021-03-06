import os
import yaml
import codecs
import discord

path = os.path.abspath(os.curdir)


def ping_has_permission(author_roles: list, target: int, pingpairs: dict):
    author_roles = [x.id for x in author_roles]
    for x in pingpairs.items():
        if x[0] in author_roles and target in x[1]:
            return True
    return False


def check_moderator(user, guild, guildroles):
    if user.guild_permissions.administrator:
        return True
    elif guild in guildroles.keys():
        for elem in guildroles[guild]['moderator']:
            if elem in [x.name for x in user.roles]:
                return True
        return False
    else:
        return 'Moderator' in [x.name for x in user.roles]


def getClientRolePosition(client):
    for x in client.roles:
        if x.name != '@everyone':
            if len(x.members) == 1 and x.members[0] == client:
                return x.position
    raise discord.InvalidData


def addPingPair(pingpairs, guild, role, target):
    if pingpairs is not None:
        if guild in pingpairs.keys():
            if role in pingpairs[guild].keys():
                if target not in pingpairs[guild][role]:
                    pingpairs[guild][role].append(target)
                else:
                    return
            else:
                pingpairs[guild][role] = [target]
        else:
            pingpairs[guild] = {role: [target]}
    else:
        pingpairs = {guild: {role: [target]}}
    writePingPair(pingpairs)


def writePingPair(pingpairs):
    with codecs.open(path + "/configuration/pingPair.yml", 'w', "utf-8") as ymlfile:
        yaml.dump(pingpairs, ymlfile, allow_unicode=True)


def writeGuildRoles(guildroles):
    with codecs.open(path + "/configuration/moderator.yml", 'w', "utf-8") as ymlfile:
        yaml.dump(guildroles, ymlfile, allow_unicode=True)
