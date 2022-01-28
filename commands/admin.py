from discord import slash_command, Option
from discord.commands import permissions
from discord.ext import commands
from discord.types.role import Role

from util.util import addPingPair, writeGuildRoles, getClientRolePosition


class Management(commands.Cog, name='Admin Commands'):
    def __init__(self, client, pingpair, guildroles):
        self.client = client
        self.pingPair = pingpair
        self.guildRoles = guildroles

    @slash_command(guild_ids=[621724759645749258], default_permission=False)
    @permissions.is_owner()
    async def default_role(self, ctx):
        """Returns set default role"""
        guild = ctx.guild

        if self.guildRoles is None:
            await ctx.respond(ctx.author.mention + "There is no default role defined for this guild.")
        elif guild.id not in self.guildRoles.keys():
            await ctx.respond(ctx.author.mention + "There is no default role defined for this guild.")
        elif 'default' not in self.guildRoles[guild.id].keys():
            await ctx.respond(ctx.author.mention + "There is no default role defined for this guild.")
        else:
            try:
                role = guild.get_role(self.guildRoles[guild.id]['default'])
                await ctx.respond(ctx.author.mention + " "
                                                       "**{}** is the default role for this guild".format(role.name))
            except:
                await ctx.respond(ctx.author.mention + "There is no default role defined for this guild.")

    @slash_command(guild_ids=[621724759645749258], default_permission=False)
    @permissions.is_owner()
    async def set_default_role(self, ctx, role: Option(Role, "Role")):
        """Sets the default role."""
        guild = ctx.guild
        role = role.id

        if self.guildRoles is None:
            self.guildRoles = {guild.id: {'default': role}}
        elif guild.id in self.guildRoles.keys():
            self.guildRoles[guild.id]['default'] = role
        else:
            self.guildRoles[guild.id] = {'default': role}

        writeGuildRoles(self.guildRoles)
        await ctx.respond(ctx.author.mention + " " +
                          str(guild.get_role(
                              self.guildRoles[guild.id]['default']).name) + " is now the default role.")

    @slash_command(guild_ids=[621724759645749258], default_permission=False)
    @permissions.is_owner()
    async def del_default_role(self, ctx):
        """Deletes the default role."""
        guild = ctx.guild

        if self.guildRoles is not None:
            if guild.id in self.guildRoles.keys():
                if 'default' in self.guildRoles[guild.id].keys():
                    del self.guildRoles[guild.id]['default']
                    writeGuildRoles(self.guildRoles)
        await ctx.respond(ctx.author.mention + " The default role was deleted.")

    @slash_command(guild_ids=[621724759645749258], default_permission=False)
    @permissions.is_owner()
    async def add_rule(self, ctx, role_1: Option(Role, "role"),
                       relation: Option(str, "relation", choices=["->", "<->", "<-"]),
                       role_2: Option(Role, "role") = None):
        """Adds a ping rule"""
        guild = ctx.guild
        client_member = guild.get_member(self.client.user.id)

        if relation == ' ' or relation == '->':
            if role_2.position < getClientRolePosition(client_member):
                addPingPair(self.pingPair, guild.id, role_1.id, role_2.id)
            else:
                await ctx.channel.send(
                    ctx.author.mention + " Bot has to be higher in the role hierarchy, as the target role",
                    delete_after=5)
                return
        elif relation == '<-':
            if role_1.position < getClientRolePosition(client_member):
                addPingPair(self.pingPair, guild.id, role_2.id, role_1.id)
            else:
                await ctx.channel.send(
                    ctx.author.mention + " Bot has to be higher in the role hierarchy, as the target role",
                    delete_after=5)
                return
        elif relation == '<->':
            pos = getClientRolePosition(client_member)
            if role_1.position < pos and role_2.position < pos:
                addPingPair(self.pingPair, guild.id, role_2.id, role_1.id)
                addPingPair(self.pingPair, guild.id, role_1.id, role_2.id)
            else:
                await ctx.respond(
                    ctx.author.mention + " Bot has to be higher in the role hierarchy, as the target role",
                    delete_after=5)
                return
        else:
            await ctx.respond(
                ctx.author.mention + " You have to give an relation between the roles (->, <-, <->)",
                delete_after=5)
            return

        await ctx.respond(ctx.author.mention +
                          " The Relation: {} ({}) {} {} ({}) has been saved".format(role_1.name,
                                                                                    role_1.id, relation,
                                                                                    role_2.name,
                                                                                    role_2.id))

    @slash_command(guild_ids=[621724759645749258], default_permission=False)
    @permissions.is_owner()
    async def add_moderator_role(self, ctx, role: Option(Role, "role")):
        """Set Moderator-Role (needed for $members and $printRules)"""
        guild = ctx.guild

        if self.guildRoles is None:
            self.guildRoles = {guild.id: {'moderator': [role.id]}}
        elif guild.id in self.guildRoles.keys():
            if 'moderator' not in self.guildRoles[guild.id].keys():
                self.guildRoles[guild.id]['moderator'] = [role.id]
            if role not in self.guildRoles[guild.id]['moderator']:
                self.guildRoles[guild.id]['moderator'].append(role.id)
        else:
            self.guildRoles[guild.id] = {'moderator': [role.id]}

        writeGuildRoles(self.guildRoles)
        await ctx.respond(ctx.author.mention + " " + ", ".join(
            [guild.get_role(x).name for x in
             self.guildRoles[guild.id]['moderator']]) + " are now the moderator roles.")

    @slash_command(guild_ids=[621724759645749258], default_permission=False)
    @permissions.is_owner()
    async def remove_moderator_role(self, ctx, role: Option(Role, "role")):
        """Remove Moderator-Role (needed for $members and $printRules)"""

        guild = ctx.guild

        if self.guildRoles is not None:
            if guild.id in self.guildRoles.keys():
                try:
                    self.guildRoles[guild.id]['moderator'].remove(role.id)
                    writeGuildRoles(self.guildRoles)

                    await ctx.respond(
                        ctx.author.mention + " " + role.name + " was removed.")
                    return

                except ValueError:
                    pass

        await ctx.respond(ctx.message.author.mention + " " + role.name + " it is not registered as a "
                                                                "moderator role.")
