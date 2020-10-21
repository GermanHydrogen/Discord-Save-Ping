import os
import yaml

path = os.path.abspath(os.curdir)


def ping_has_permission(author_roles, target, pingpairs):
    author_roles = [x.name for x in author_roles]
    for x in pingpairs.items():
        if x[0] in author_roles and target in x[1]:
            return True
    return False


def check_moderator(user, guild, moderatorroles):
    if guild in moderatorroles.keys():
        return moderatorroles[guild] in [x.name for x in user.roles] or user.guild_permissions.administrator
    else:
        return 'Moderator' in [x.name for x in user.roles] or user.guild_permissions.administrator


def addPingPair(pingpairs, guild,role, target):
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
    print(pingpairs)

    writePingPair(pingpairs)


def writePingPair(pingpairs):
    with open(path + "/configuration/pingPair.yml", 'w') as ymlfile:
        yaml.dump(pingpairs, ymlfile)


def writeModeratorRoles(moderatorroles):
    with open(path + "/configuration/moderator.yml", 'w') as ymlfile:
        yaml.dump(moderatorroles, ymlfile)