import discord
from loader import cfg

from discord.ext import commands
from discord.ext.commands import Bot, has_role

client = Bot(command_prefix="$", case_insensitive=True)


@client.event
async def on_command_error(ctx, error):
    if ctx.message.channel != "DMChannel" and ctx.message.channel != "GroupChannel":
        await ctx.message.delete()

    if isinstance(error, commands.errors.MissingRole):
        await ctx.message.channel.send(ctx.message.author.mention + " You don't have sufficient permissions!",
                                       delete_after=5)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.message.channel.send(ctx.message.author.mention + " Missing parameters!",
                                       delete_after=5)
    else:
        await ctx.send(ctx.message.author.mention + " Command not found! Check **!help** for all commands",
                       delete_after=5)
        raise error


@client.command()
@has_role(cfg['role'])
async def ping(ctx, role):
    guild = ctx.message.guild
    match = [x for x in guild.roles if x.name == role]
    if len(match) == 1:
        if match[0] in cfg['pingable']:
            await match[0].edit(mentionable=True)
            await ctx.channel.send(match[0].mention)
            await match[0].edit(mentionable=False)
        else:
            await ctx.channel.send(ctx.message.author.mention + " You can't mention this role", delete_after=5)
    else:
        await ctx.channel.send(ctx.message.author.mention + " Role not Found", delete_after=5)

    await ctx.message.delete()


@client.command()
@has_role(cfg['role'])
async def members(ctx, role):
    guild = ctx.message.guild
    match = [x for x in guild.roles if x.name == role]
    if len(match) == 1:
        user = "\n".join(x.name + '#' + x.discriminator + "\t" + x.mention for x in match[0].members)

        embed = discord.Embed(title="Members of **" + match[0].name + "**", type='article', color=match[0].colour,
                              description="**Found " + str(len(match[0].members)) + " User**\n\n" + user)
        await ctx.channel.send(embed=embed)

    else:
        await ctx.channel.send(ctx.message.author.mention + " Role not Found", delete_after=5)

    await ctx.message.delete()

client.run(cfg['token'])
