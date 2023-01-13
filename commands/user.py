import discord
from discord import errors, slash_command, Option
from discord.ext import commands
from util.util import ping_has_permission


class User(commands.Cog, name='User Commands'):
    def __init__(self, client, pingPair, logger):
        self.client = client
        self.pingPair = pingPair
        self.logger = logger

    async def role_searcher(self, ctx: discord.AutocompleteContext):
        roles = [role for role in self.pingPair[ctx.interaction.guild.id].values()]

        roles = [discord.utils.get(ctx.interaction.guild.roles, id=role) for sublist in roles for role in sublist
                 if ping_has_permission(ctx.interaction.user.roles, role, self.pingPair[ctx.interaction.guild.id])]

        return [role.name for role in roles if role.name.lower().startswith(ctx.value.lower())]

    @slash_command()
    async def ping(self, ctx, role: Option(str, "Role", autocomplete=role_searcher)):
        """Ping a role via the bot"""
        guild = ctx.guild
        match = discord.utils.get(guild.roles, name=role)
        if match:
            if ping_has_permission(ctx.author.roles, match.id, self.pingPair[ctx.guild.id]):
                preState = match.mentionable
                try:
                    await match.edit(mentionable=True)
                    try:
                        await ctx.send(match.mention)
                        await ctx.respond('Done', delete_after=3)
                        log = "Guild: " + str(ctx.guild.name).ljust(20) + "\t"
                        log += "User: " + str(ctx.author).ljust(20) + "\t"
                        log += "Channel:" + str(ctx.channel).ljust(20) + "\t"
                        log += "Command: " + str(ctx.content).ljust(20) + "\t"

                        self.logger.info(log)
                    except:
                        pass
                    await match.edit(mentionable=preState)
                except errors.Forbidden:
                    await ctx.respond(ctx.author.mention + " Configuration Error, please contact your "
                                                           "Admin", delete_after=5)
            else:
                await ctx.respond(ctx.author.mention + " You can't mention this role", delete_after=5)
        else:
            await ctx.respond(ctx.author.mention + " Role not Found", delete_after=5)

    @slash_command()
    async def ping_vc(self, ctx):
        """Ping all members of your voice channel"""
        if ctx.author.voice is None:
            await ctx.respond("You have to be in a voice channel for this command to work!", delete_after=5)
            return

        await ctx.respond(" ".join([x.mention for x in ctx.author.voice.channel.members]))
