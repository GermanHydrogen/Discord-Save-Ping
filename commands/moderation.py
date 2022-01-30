import discord
from discord import slash_command, Option
from discord.ext import commands
from discord.types.role import Role

from util.util import check_moderator


class Moderation(commands.Cog, name='Moderation Commands'):
    def __init__(self, client, pingPair, guildroles):
        self.client = client
        self.pingPair = pingPair
        self.moderatorRoles = guildroles

    @slash_command()
    async def print_rules(self, ctx):
        """Shows all ping rules for this guild'"""
        guild = ctx.guild
        # Check Permission
        if not check_moderator(ctx.author, guild.id, self.moderatorRoles):
            raise commands.errors.MissingPermissions(['owner'])

        if self.pingPair is None or guild.id not in self.pingPair.keys():
            await ctx.respond(
                ctx.author.mention + " There are currently no rules active in this guild.",
                delete_after=5)
            return

        output = "\n\n".join(["**" + guild.get_role(int(x[0])).name + ":**\n" + "\n".join(["----> " + guild.get_role(int(y)).name for y in x[1]]) for x in
                              self.pingPair[guild.id].items()])

        embed = discord.Embed(title="**Ping Rules**", description=output, color=ctx.author.color)
        embed.set_author(name=ctx.author.display_name)
        embed.set_footer(text='[User with this role can ping] ----> [this role]',
                         icon_url=guild.icon.url)

        await ctx.respond(embed=embed)

    @slash_command()
    async def members(self, ctx, role: Option(Role, "Role")):
        """Shows all members of a role"""

        guild = ctx.guild
        # Check Permission
        if not check_moderator(ctx.author, guild.id, self.moderatorRoles):
            raise commands.errors.MissingPermissions(['owner'])

        user = "\n".join(x.name + '#' + x.discriminator + "\t" + x.mention for x in role.members)
        embed = discord.Embed(title="Members of **" + role.name + "**", type='article', color=role.colour,
                              description="**Found " + str(len(role.members)) + " User**\n\n" + user)
        await ctx.respond(embed=embed)

