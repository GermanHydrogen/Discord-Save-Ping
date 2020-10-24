import discord
from discord.ext import commands
from discord.ext.commands import Bot, HelpCommand

from commands.admin import Managment
from commands.moderation import Moderation
from commands.user import User
from util.loader import cfg, pingPair, moderatorRoles

intents = discord.Intents.default()
intents.members = True
client = Bot(command_prefix=cfg['prefix'], case_insensitive=True, intents=intents)


@client.event
async def on_ready():
    game = discord.Game(name="https://github.com/GermanHydrogen/Discord-Save-Ping")
    await client.change_presence(activity=game)


@client.event
async def on_command_error(ctx, error):
    if ctx.message.channel != "DMChannel" and ctx.message.channel != "GroupChannel":
        await ctx.message.delete()

    if isinstance(error, commands.errors.MissingRole) or isinstance(error, commands.errors.MissingPermissions):
        await ctx.message.channel.send(ctx.message.author.mention + " You don't have sufficient permissions!",
                                       delete_after=5)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.message.channel.send(ctx.message.author.mention + " Missing parameters!",
                                       delete_after=5)
    else:
        await ctx.send(ctx.message.author.mention + " Command not found! Check **!help** for all commands",
                       delete_after=5)
        raise error


client.add_cog(User(client, pingPair))
client.add_cog(Moderation(client, pingPair, moderatorRoles))
client.add_cog(Managment(client, pingPair, moderatorRoles))

client.run(cfg['token'])
