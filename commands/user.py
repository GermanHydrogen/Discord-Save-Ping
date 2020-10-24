import discord
from discord import errors
from discord.ext import commands
from util.util import ping_has_permission


class User(commands.Cog, name='User Commands'):
    def __init__(self, client, pingPair):
        self.client = client
        self.pingPair = pingPair

    @commands.command(help='Pings the specified role', usage='[role name]', category='User')
    async def ping(self, ctx, role):
        guild = ctx.message.guild
        match = discord.utils.get(guild.roles, name=role)
        if match:
            if ping_has_permission(ctx.message.author.roles, match.id, self.pingPair[ctx.message.guild.id]):
                preState = match.mentionable
                try:
                    await match.edit(mentionable=True)
                    try:
                        await ctx.channel.send(match.mention)
                    except:
                        pass
                    await match.edit(mentionable=preState)
                except errors.Forbidden:
                    await ctx.channel.send(ctx.message.author.mention + " Configuration Error, please contact your "
                                                                        "Admin", delete_after=5)
            else:
                await ctx.channel.send(ctx.message.author.mention + " You can't mention this role", delete_after=5)
        else:
            await ctx.channel.send(ctx.message.author.mention + " Role not Found", delete_after=5)

        await ctx.message.delete()