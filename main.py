import discord
import re
from loader import cfg, pingPair, moderatorRoles
from util import ping_has_permission, addPingPair, writeModeratorRoles, check_moderator

from discord.ext import commands
from discord.ext.commands import Bot, has_role, has_permissions

client = Bot(command_prefix="$", case_insensitive=True)

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


@client.command(help='Pings the specified role', usage='[role name]', category='User')
async def ping(ctx, role):
    guild = ctx.message.guild
    match = [x for x in guild.roles if x.name == role]
    if len(match) == 1:
        if ping_has_permission(ctx.message.author.roles, str(match[0]), pingPair[ctx.message.guild.id]):
            await match[0].edit(mentionable=True)
            await ctx.channel.send(match[0].mention)
            await match[0].edit(mentionable=False)
        else:
            await ctx.channel.send(ctx.message.author.mention + " You can't mention this role", delete_after=5)
    else:
        await ctx.channel.send(ctx.message.author.mention + " Role not Found", delete_after=5)

    await ctx.message.delete()


@client.command(help='Adds a ping rule',
                usage='[mention role 1] [relation] [mention role 2]  | relation can be ->, <-, <->',
                category='Admin')
@has_permissions(administrator=True)
async def addRule(ctx):
    guild = ctx.message.guild.id
    msg = ctx.message.content.replace('$addRule', "").strip()
    mentions = ctx.message.role_mentions
    if len(mentions) != 2:
        await ctx.channel.send(ctx.message.author.mention + " Please give two Roles as mentions", delete_after=5)

    relation = msg.replace(mentions[0].mention, "").replace(mentions[1].mention, "").strip()

    if relation == '':
        relation = ' '

    print(msg.split(relation))

    # Order
    mentions = {str(x.id): x.name for x in mentions}
    mentions = [mentions[re.sub("[^0-9]", "", x)] for x in msg.split(relation)]

    if relation == ' ' or relation == '->':
        addPingPair(pingPair, guild, mentions[0], mentions[1])
    elif relation == '<-':
        addPingPair(pingPair, guild, mentions[1], mentions[0])
    elif relation == '<->':
        addPingPair(pingPair, guild, mentions[1], mentions[0])
        addPingPair(pingPair, guild, mentions[0], mentions[1])
    else:
        await ctx.channel.send(
            ctx.message.author.mention + " You have to give an relation between the roles (->, <-, <->)",
            delete_after=5)
        await ctx.message.delete()
        return

    await ctx.channel.send(ctx.message.author.mention + " The Relation: {} {} {} has been saved".format(mentions[0],
                                                                                                        relation,
                                                                                                        mentions[1]))
    await ctx.message.delete()


@client.command(help='Shows all ping rules for this guild (Moderators only)', usage='')
async def printRules(ctx):
    guild = ctx.message.guild.id
    # Check Permission
    if not check_moderator(ctx.message.author, guild, moderatorRoles):
        raise commands.errors.MissingRole

    if guild not in pingPair.keys():
        await ctx.channel.send(
            ctx.message.author.mention + " There are currently no rules active in this guild.",
            delete_after=5)

    output = "\n\n".join(["**" + x[0] + ":**\n" + "\n".join(["----> " + y for y in x[1]]) for x in pingPair[ctx.message.guild.id].items()])

    embed = discord.Embed(title="**Ping Rules**", description=output, color=ctx.message.author.color)
    embed.set_author(name=ctx.message.author.display_name, icon_url=str(ctx.message.author.avatar_url))
    embed.set_footer(text='[User with this role can ping] ----> [this role]', icon_url='https://media.discordapp.net/attachments/664892036171825156/665328124187115520/Logo_RR_2020.png?width=684&height=678')

    await ctx.channel.send(embed=embed)

    await ctx.message.delete()


@client.command(help='Set Moderator-Role (needed for $members and $printRules)',
                usage='[role name]',
                category='Admin')
@has_permissions(administrator=True)
async def setModeratorRole(ctx, role):
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


@client.command(help='Shows all members of a role (Moderators only)', usage='[role name]')
async def members(ctx, role):
    guild = ctx.message.guild
    # Check Permission
    if not check_moderator(ctx.message.author, guild.id, moderatorRoles):
        raise commands.errors.MissingRole

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
