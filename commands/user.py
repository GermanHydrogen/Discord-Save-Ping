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
        match = [x for x in guild.roles if x.name == role]
        if len(match) == 1:
            if ping_has_permission(ctx.message.author.roles, str(match[0]), self.pingPair[ctx.message.guild.id]):
                preState = match[0].mentionable
                try:
                    await match[0].edit(mentionable=True)
                    await ctx.channel.send(match[0].mention)
                    await match[0].edit(mentionable=preState)
                except errors.Forbidden:
                    await ctx.channel.send(ctx.message.author.mention + " Configuration Error, please contact your "
                                                                        "Admin", delete_after=5)
            else:
                await ctx.channel.send(ctx.message.author.mention + " You can't mention this role", delete_after=5)
        else:
            await ctx.channel.send(ctx.message.author.mention + " Role not Found", delete_after=5)

        await ctx.message.delete()