import logging
import datetime
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot, HelpCommand

from commands.admin import Managment
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

                role = guild.get_role(guildRoles[guild.id]['default'])
                if not role:
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

    log = "Guild: " + str(ctx.message.guild.name).ljust(20) + "\t"
    log += "User: " + str(ctx.message.author).ljust(20) + "\t"
    log += "Channel:" + str(ctx.message.channel).ljust(20) + "\t"
    log += "Command: " + str(ctx.message.content).ljust(20) + "\t"
    log += str(error)

    logger.error(log)

    raise error


@client.event
async def on_member_join(member):
    guild = member.guild
    if guildRoles is None:
        pass
    elif guild.id not in guildRoles.keys():
        pass
    elif 'default' not in guildRoles[guild.id].keys():
        pass
    else:
        role = guild.get_role(guildRoles[guild.id]['default'])
        if role is None:
            logger.error(f"Role {guildRoles[guild.id]['default']} in guild {guild.name} not found.")
        else:
            try:
                await member.add_roles(role)
                log = "Guild: " + str(guild.name).ljust(20) + "\t"
                log += "Role: " + str(role.name).ljust(20) + "\t"
                log += "User: " + str(member.display_name).ljust(20) + "\t"
                log += "Added Role succesfully"

                logger.info(log)

            except discord.Forbidden and discord.HTTPException as e:
                log = f"Adding Role failed for guild {guild.name} and role {guild.name}" + "\t"
                log += str(e)
                logger.error(log)
                raise e

client.add_cog(User(client, pingPair, logger))
client.add_cog(Moderation(client, pingPair, guildRoles))
client.add_cog(Managment(client, pingPair, guildRoles))

client.run(cfg['token'])
