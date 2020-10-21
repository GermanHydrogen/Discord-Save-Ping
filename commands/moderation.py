import discord
from discord.ext import commands
from util.util import check_moderator


class Moderation(commands.Cog, name='Moderation Commands'):
    def __init__(self, client, pingPair, moderatorRoles):
        self.client = client
        self.pingPair = pingPair
        self.moderatorRoles = moderatorRoles

    @commands.command(help='Shows all ping rules for this guild', usage='')
    async def printRules(self, ctx):
        guild = ctx.message.guild.id
        # Check Permission
        if not check_moderator(ctx.message.author, guild, self.moderatorRoles):
            raise commands.errors.MissingRole

        if guild not in self.pingPair.keys():
            await ctx.channel.send(
                ctx.message.author.mention + " There are currently no rules active in this guild.",
                delete_after=5)

        output = "\n\n".join(["**" + x[0] + ":**\n" + "\n".join(["----> " + y for y in x[1]]) for x in
                              self.pingPair[ctx.message.guild.id].items()])

        embed = discord.Embed(title="**Ping Rules**", description=output, color=ctx.message.author.color)
        embed.set_author(name=ctx.message.author.display_name, icon_url=str(ctx.message.author.avatar_url))
        embed.set_footer(text='[User with this role can ping] ----> [this role]',
                         icon_url='https://media.discordapp.net/attachments/664892036171825156/665328124187115520/Logo_RR_2020.png?width=684&height=678')

        await ctx.channel.send(embed=embed)

        await ctx.message.delete()

    @commands.command(help='Shows all members of a role', usage='[role name]')
    async def members(self, ctx, role):
        guild = ctx.message.guild
        # Check Permission
        if not check_moderator(ctx.message.author, guild.id, self.moderatorRoles):
            raise commands.errors.MissingRole

        match = discord.utils.get(guild.roles, name=role)
        if match:
            user = "\n".join(x.name + '#' + x.discriminator + "\t" + x.mention for x in match.members)
            print(match.members)
            embed = discord.Embed(title="Members of **" + match.name + "**", type='article', color=match.colour,
                                  description="**Found " + str(len(match.members)) + " User**\n\n" + user)
            await ctx.channel.send(embed=embed)

        else:
            await ctx.channel.send(ctx.message.author.mention + " Role not Found", delete_after=5)

        await ctx.message.delete()