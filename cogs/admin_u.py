import discord
from discord.ext import commands
from cogs.db import dbconn
import time
from discord.utils import get

class admin_u(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db_conn = dbconn()
        self.embed = None

    def create_embed(self, color, msg, author_name, icon):
        self.embed = discord.Embed(color=color, description=msg)
        self.embed.set_author(name=author_name,icon_url=icon)

    def get_userId_from_name(self, ctx, member : str):
        tar_member = None
        member_name = member.split("#")[0]
        member_disc = member.split("#")[1]
        for member in  ctx.guild.members:
            if member.name == member_name and member.discriminator == member_disc:
                tar_member = member
        return tar_member

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role('Omega')
    async def ubal(self, ctx, member, amount : int):
        if "@" not in member:
            member = f'<@!{self.get_userId_from_name(ctx, member).id}>'
        author_name = "Admin Command <Update Balance>"
        if '!' not in member:
            member = member[:2] + '!' + member[2:]
        self.db_conn.dbconn_open()
        self.db_conn.update_bal(f'{ctx.author}', member, amount)
        self.db_conn.dbconn_close()
        self.create_embed(0xff8080, f'**Updated Balance for {member}**', author_name, ctx.guild.icon_url)
        await ctx.send(embed=self.embed)

    #error handling for ubal
    @ubal.error
    async def ubal_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Enter the right command .ubal <@user> <amount>')
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role('Omega')
    async def dbq(self, ctx, mode: int, db_query : str):
        author_name = "Admin Command <DB Access>"
        self.db_conn.dbconn_open()
        #get
        results = self.db_conn.db_exec(mode, db_query)
        self.db_conn.dbconn_close()
        self.create_embed(0xff8080, "Query Executed and Returned", author_name, ctx.guild.icon_url)
        await ctx.send(embed=self.embed)
        await ctx.author.send(results)

    #error handling for dbq
    @dbq.error
    async def dbq_error(self,ctx, error):
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role('Omega')
    async def u_role(self, ctx, member, role : discord.Role):
        if "@" not in member:
            member = self.get_userId_from_name(ctx, member)
        else:
            if '!' not in member:
                member = member[:2] + '!' + member[2:]
            member = await ctx.guild.fetch_member(int(member[3:-1]))

        author_name = "Admin Command <Update Role>"
        for m_role in member.roles[1:]:
            await member.remove_roles(m_role)
        await member.add_roles(role)
        userId = f'<@!{member.id}>'
        self.db_conn.dbconn_open()
        self.db_conn.update_role(userId, role.name)
        self.create_embed(0xff8080, "**Rank Updated**", author_name, ctx.guild.icon_url)
        await ctx.send(embed=self.embed)
        self.db_conn.dbconn_close()

    #error handling for u_role
    @u_role.error
    async def u_role_error(self,ctx, error):
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')

def setup(client):
    client.add_cog(admin_u(client))
    print("Cog - \"Admin_Utils\" Loaded")
