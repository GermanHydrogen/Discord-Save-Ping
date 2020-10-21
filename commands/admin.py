import re
from discord.ext import commands
from util.util import addPingPair, writeModeratorRoles, getClientRolePosition
from discord.ext.commands import has_permissions


class Managment(commands.Cog, name='Admin Commands'):
    def __init__(self, client, pingpair, moderatorroles):
        self.client = client
        self.pingPair = pingpair
        self.moderationRoles = moderatorroles

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
                addPingPair(self.pingPair, guild.id, mentions[0].name, mentions[1].name)
            else:
                await ctx.channel.send(
                    ctx.message.author.mention + " Bot has to be higher in the role hierarchy, as the target role",
                    delete_after=5)
                await ctx.message.delete()
                return
        elif relation == '<-':
            if mentions[0].position < getClientRolePosition(clientMember):
                addPingPair(self.pingPair, guild.id, mentions[1].name, mentions[0].name)
            else:
                await ctx.channel.send(
                    ctx.message.author.mention + " Bot has to be higher in the role hierarchy, as the target role",
                    delete_after=5)
                await ctx.message.delete()
                return
        elif relation == '<->':
            pos = getClientRolePosition(clientMember)
            if mentions[0].position < pos and mentions[1].position < pos:
                addPingPair(self.pingPair, guild.id, mentions[1].name, mentions[0].name)
                addPingPair(self.pingPair, guild.id, mentions[0].name, mentions[1].name)
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

        await ctx.channel.send(ctx.message.author.mention + " The Relation: {} {} {} has been saved".format(mentions[0].name,
                                                                                                            relation,
                                                                                                            mentions[
                                                                                                                1].name))
        await ctx.message.delete()

    @commands.command(help='Set Moderator-Role (needed for $members and $printRules)',
                      usage='[role name]',
                      category='Admin')
    @has_permissions(administrator=True)
    async def setModeratorRole(self, ctx, role):
        global moderatorRoles
        guild = ctx.message.guild
        match = [x for x in guild.roles if x.name == role]

        if len(match) == 1:
            if moderatorRoles is None:
                moderatorRoles = {guild.id: role}
            else:
                moderatorRoles[guild.id] = role

            writeModeratorRoles(moderatorRoles)
            await ctx.channel.send(ctx.message.author.mention + " " + role + " is now the moderator role.")
        else:
            await ctx.channel.send(ctx.message.author.mention + " Role not Found", delete_after=5)

        await ctx.message.delete()