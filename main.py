import logging
import datetime
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot, HelpCommand

from commands.admin import Management
from commands.moderation import Moderation
from commands.user import User
from util.loader import cfg, pingPair, guildRoles

intents = discord.Intents.default()
intents.members = True
client = Bot(command_prefix=cfg['prefix'], case_insensitive=True, intents=intents)

# init logger
path = os.path.dirname(os.path.abspath(__file__))

TODAY = datetime.date.today()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=path + f"/logs/{TODAY}.log", encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
logger.addHandler(handler)

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.DEBUG)
discord_handler = logging.FileHandler(filename=path + '/logs/discord.log', encoding='utf-8', mode='w')
discord_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
discord_logger.addHandler(discord_handler)


@client.event
async def on_ready():
    for guild_id in guildRoles:
        guild = client.get_guild(guild_id)
        if guild is None:
            print(f"Error: Guild not found: {guild_id}")
            logger.error(f"Error: Guild not found: {guild_id}")
        else:
            member = guild.get_member(client.user.id)
            if member is not None:
                if not member.guild_permissions.manage_roles:
                    print(f"Error: Not sufficient permissions for {guild.name}")
                    logger.error(f"Error: Not sufficient permissions for {guild.name}")

                if 'default' in guildRoles[guild.id]:
                    if not (role := guild.get_role(guildRoles[guild.id]['default'])):
                        print(f"Error: Role {guildRoles[guild.id]['default']} not found for {guild.name}")
                        logger.error("Error: Role {guildRoles[guild.id]['default']} not found for {guild.name}")
                    else:
                        if member.top_role.position < role.position:
                            print(f"Error: Bot role has to be higher then the default role "
                                  f"{role.name} in guild {guild.name}")
                            logger.error("Error: Bot role has to be higher then the default role "
                                         f"{role.name} in guild {guild.name}")

    print("Ready")
    game = discord.Game(name="https://github.com/GermanHydrogen/Discord-Save-Ping")
    await client.change_presence(activity=game)
    logger.info("Server Started")


@client.event
async def on_application_command_error(ctx, error):
    print(type(error))
    if isinstance(error.original, commands.errors.MissingRole) or isinstance(error.original, commands.errors.MissingPermissions):
        await ctx.respond(ctx.author.mention + " You don't have sufficient permissions!",
                                       delete_after=5)
    elif isinstance(error.original, commands.errors.MissingRequiredArgument):
        await ctx.respond(ctx.author.mention + " Missing parameters!",
                                       delete_after=5)
    else:
        await ctx.respond(ctx.author.mention + " An error occurred, please contact your local admin.",
                       delete_after=5)

    log = "Guild: " + str(ctx.guild.name).ljust(20) + "\t"
    log += "User: " + str(ctx.author).ljust(20) + "\t"
    log += "Channel:" + str(ctx.channel).ljust(20) + "\t"
    log += "Command: " + str(ctx.command).ljust(20) + "\t"
    log += str(error)

    logger.error(log)

    raise error



client.add_cog(User(client, pingPair, logger))
client.add_cog(Moderation(client, pingPair, guildRoles))
client.add_cog(Management(client, pingPair, guildRoles))

client.run(cfg['token'])
