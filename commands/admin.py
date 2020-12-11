import re
import discord
from discord.ext import commands
from util.util import addPingPair, writeGuildRoles, getClientRolePosition
from discord.ext.commands import has_permissions


class Managment(commands.Cog, name='Admin Commands'):
    def __init__(self, client, pingpair, guildroles):
        self.client = client
        self.pingPair = pingpair
        self.guildRoles = guildroles

    @commands.command(help='Returns set default role',
                      usage='',
                      category='Admin')
    async def defaultRole(self, ctx):
        guild = ctx.message.guild

        if self.guildRoles is None:
            ctx.channel.send(ctx.message.author.mention + "There is no default role defined for this guild.")
        elif guild.id not in self.guildRoles.keys():
            ctx.channel.send(ctx.message.author.mention + "There is no default role defined for this guild.")
        elif 'default' not in self.guildRoles[guild.id].keys():
            ctx.channel.send(ctx.message.author.mention + "There is no default role defined for this guild.")
        else:
            try:
                role = guild.get_role(self.guildRoles[guild.id]['default'])
                await ctx.channel.send(ctx.message.author.mention + " "
                                       "**{}** is the default role for this guild".format(role.name))
            except:
                ctx.channel.send(ctx.message.author.mention + "There is no default role defined for this guild.")

        await ctx.message.delete()

    @commands.command(help='Sets a default role. If no role is specified, the attribute default role is cleared!',
                      usage='[role name] opt',
                      category='Admin')
    async def setDefaultRole(self, ctx):
        argv = ctx.message.content.split(" ")
        role = " ".join(argv[1:])

        guild = ctx.message.guild

        if role.strip() == "":
            match = None
        else:
            match = discord.utils.get(guild.roles, name=role)

        if match:   # Sets the default role
            role = match.id

            if self.guildRoles is None:
                self.guildRoles = {guild.id: {'default': role}}
            elif guild.id in self.guildRoles.keys():
                self.guildRoles[guild.id]['default'] = role
            else:
                self.guildRoles[guild.id] = {'default': role}

            writeGuildRoles(self.guildRoles)
            await ctx.channel.send(ctx.message.author.mention + " " +
                                   str(guild.get_role(
                                       self.guildRoles[guild.id]['default']).name) + " is now the default role.")
        elif role.strip() == "":    # Resets the default role
            if self.guildRoles is not None:
                if guild.id in self.guildRoles.keys():
                    if 'default' in self.guildRoles[guild.id].keys():
                        del self.guildRoles[guild.id]['default']
                        writeGuildRoles(self.guildRoles)
                        await ctx.channel.send(ctx.message.author.mention + " The default role was deleted.")
        else:
            await ctx.channel.send(ctx.message.author.mention + " Role not Found", delete_after=5)

        await ctx.message.delete()

    @commands.command(help='Adds a ping rule',
                      usage='[mention role 1] [relation] [mention role 2]  | relation can be ->, <-, <->',
                      category='Admin')
    @has_permissions(administrator=True)
    async def addRule(self, ctx):
        guild = ctx.message.guild
        clientMember = guild.get_member(self.client.user.id)

        msg = ctx.message.content.replace('$addRule', "").strip()
        mentions = ctx.message.role_mentions
        if len(mentions) != 2:
            await ctx.channel.send(ctx.message.author.mention + " Please give two Roles as mentions", delete_after=5)
            await ctx.message.delete()
            return

        relation = msg.replace(mentions[0].mention, "").replace(mentions[1].mention, "").strip()

        if relation == '':
            relation = ' '

        # Order
        mentions = {str(x.id): x for x in mentions}
        mentions = [mentions[re.sub("[^0-9]", "", x)] for x in msg.split(relation)]

        if relation == ' ' or relation == '->':
            if mentions[1].position < getClientRolePosition(clientMember):
                addPingPair(self.pingPair, guild.id, mentions[0].id, mentions[1].id)
            else:
                await ctx.channel.send(
                    ctx.message.author.mention + " Bot has to be higher in the role hierarchy, as the target role",
                    delete_after=5)
                await ctx.message.delete()
                return
        elif relation == '<-':
            if mentions[0].position < getClientRolePosition(clientMember):
                addPingPair(self.pingPair, guild.id, mentions[1].id, mentions[0].id)
            else:
                await ctx.channel.send(
                    ctx.message.author.mention + " Bot has to be higher in the role hierarchy, as the target role",
                    delete_after=5)
                await ctx.message.delete()
                return
        elif relation == '<->':
            pos = getClientRolePosition(clientMember)
            if mentions[0].position < pos and mentions[1].position < pos:
                addPingPair(self.pingPair, guild.id, mentions[1].id, mentions[0].id)
                addPingPair(self.pingPair, guild.id, mentions[0].id, mentions[1].id)
            else:
                await ctx.channel.send(
                    ctx.message.author.mention + " Bot has to be higher in the role hierarchy, as the target role",
                    delete_after=5)
                await ctx.message.delete()
                return
        else:
            await ctx.channel.send(
                ctx.message.author.mention + " You have to give an relation between the roles (->, <-, <->)",
                delete_after=5)
            await ctx.message.delete()
            return

        await ctx.channel.send(ctx.message.author.mention +
                               " The Relation: {} ({}) {} {} ({}) has been saved".format(mentions[0].name,
                                                                                         mentions[0].id, relation,
                                                                                         mentions[1].name,
                                                                                         mentions[1].id))
        await ctx.message.delete()

    @commands.command(help='Set Moderator-Role (needed for $members and $printRules)',
                      usage='[role name]',
                      category='Admin')
    @has_permissions(administrator=True)
    async def addModeratorRole(self, ctx):
        argv = ctx.message.content.split(" ")
        if len(argv) < 2:
            await ctx.channel.send(ctx.message.author.mention + " Please declare a role you want to ping!")
        role = " ".join(argv[1:])

        guild = ctx.message.guild

        match = discord.utils.get(guild.roles, name=role)
        if match:
            role = match.id

            if self.guildRoles is None:
                self.guildRoles = {guild.id: {'moderator': [role]}}
            elif guild.id in self.guildRoles.keys():
                if 'moderator' not in self.guildRoles[guild.id].keys():
                    self.guildRoles[guild.id]['moderator'] = [role]
                if role not in self.guildRoles[guild.id]['moderator']:
                    self.guildRoles[guild.id]['moderator'].append(role)
            else:
                self.guildRoles[guild.id] = {'moderator': [role]}

            writeGuildRoles(self.guildRoles)
            await ctx.channel.send(ctx.message.author.mention + " " + ", ".join(
                [guild.get_role(x).name for x in
                 self.guildRoles[guild.id]['moderator']]) + " are now the moderator roles.")
        else:
            await ctx.channel.send(ctx.message.author.mention + " Role not Found", delete_after=5)

        await ctx.message.delete()

    @commands.command(help='Remove Moderator-Role (needed for $members and $printRules)',
                      usage='[role name]',
                      category='Admin')
    @has_permissions(administrator=True)
    async def removeModeratorRole(self, ctx):
        argv = ctx.message.content.split(" ")
        if len(argv) < 2:
            await ctx.channel.send(ctx.message.author.mention + " Please declare a role you want to ping!")
        role = " ".join(argv[1:])

        guild = ctx.message.guild

        match = discord.utils.get(guild.roles, name=role)
        if match:
            role = match.id

            if self.guildRoles is not None:
                if guild.id in self.guildRoles.keys():
                    try:
                        self.guildRoles[guild.id]['moderator'].remove(role)
                        writeGuildRoles(self.guildRoles)

                        await ctx.channel.send(
                            ctx.message.author.mention + " " + guild.get_role(role).name + " was removed.")
                        await ctx.message.delete()
                        return

                    except ValueError:
                        pass

        await ctx.channel.send(ctx.message.author.mention + " " + role + " it is not registered as a "
                                                                         "moderator role.")
        await ctx.message.delete()
