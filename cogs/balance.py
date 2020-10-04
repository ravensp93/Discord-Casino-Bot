import discord
from discord.ext import commands
from cogs.db import dbconn
import time
from discord.utils import get

class Balance(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db_conn = dbconn()
        self.guild = None
        self.currency_name = "ZEN"
        self.embed = None


    def create_embed(self, color, msg, author_name, icon):
        self.embed = discord.Embed(color=color, description=msg)
        self.embed.set_author(name=author_name,icon_url=icon)


    #transfer command
    @commands.command()
    @commands.guild_only()
    async def trans(self, ctx, member, amount : int):
        author_name = "Transfer Request"
        src_userId = f'<@!{ctx.author.id}>'
        if '!' not in member:
            member = member[:2] + '!' + member[2:]
        if(src_userId == member):
            self.create_embed(0xfffff1, "You can\'t transfer to yourself!", author_name, ctx.guild.icon_url)
            await ctx.send(embed=self.embed)
            return

        self.db_conn.dbconn_open()

        if(amount > 0):
            if(self.db_conn.withdraw_bal(src_userId, amount)):
                self.db_conn.deposit_bal(member, amount)
                txt = f'{src_userId} tranferred **{amount} {self.currency_name}** to {member}\'s wallet.'
                self.create_embed(0xfffff1, txt, author_name, ctx.guild.icon_url)
                await ctx.send(embed=self.embed)
            else:
                self.create_embed(0xfffff1, 'You have insufficient balance!', author_name, ctx.guild.icon_url)
                # embed.set_footer(text='You have insufficient balance!')
                await ctx.send(embed=self.embed)
        else:
                self.create_embed(0xfffff1, 'Invalid negative transfer!', author_name, ctx.guild.icon_url)
                await ctx.send(embed=self.embed)

        self.db_conn.dbconn_close()

    #error handling for transfer
    @trans.error
    async def trans_error(self,ctx, error):
        author_name = "Transfer Request"
        src_userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.MissingRequiredArgument):
            self.create_embed(0xfffff1, 'Enter the right command .trans <@user> <amount>' , author_name, ctx.guild.icon_url)
            await ctx.send(embed=self.embed)
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')

    #balance command
    @commands.command(name="w")
    @commands.guild_only()
    async def check_balance(self, ctx):

        userId = f'<@!{ctx.author.id}>'
        self.db_conn.dbconn_open()
        balance = self.db_conn.get_current_balance(userId)
        self.db_conn.dbconn_close()
        #retrieve guild object
        self.guild = await self.client.fetch_guild(self.client.guilds[0].id)
        #retrieve member obj using guild obj
        current_member = await self.guild.fetch_member(ctx.author.id)
        #retrieve name using member obj
        name = current_member.name
        author_name=f'{name}\'s Wallet'
        #setup embedding
        embed = discord.Embed(color=0xfffff1)
        self.create_embed(0xfffff1,"",author_name,current_member.avatar_url)
        self.embed.add_field(name=self.currency_name, value=balance, inline=False)
        #retrieve
        await ctx.author.send(embed=self.embed)

    #error handling for check_balance
    @check_balance.error
    async def check_balance_error(self,ctx, error):
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')

    #Profile command
    @commands.command(name="stats")
    @commands.guild_only()
    async def check_stats(self, ctx):
        userId = f'<@!{ctx.author.id}>'
        self.db_conn.dbconn_open()
        stats_dict = self.db_conn.get_stats(userId)
        self.db_conn.dbconn_close()
        #retrieve guild object
        self.guild = await self.client.fetch_guild(self.client.guilds[0].id)
        #retrieve member obj using guild obj
        current_member = await self.guild.fetch_member(ctx.author.id)
        #retrieve name using member obj
        author_name = f'{current_member.name}\'s Profile'
        #setup embedding
        if stats_dict != "Error":
            # self.embed.add_field(name="Total Bet", value=f'PLACEHOLDER  <:omega:755823479110107138>', inline=True)
            if stats_dict["roles"] == "Omega":
                self.create_embed(0xff8080, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'<:omega:755823479110107138> **OMEGA** <:omega:755823479110107138>', inline=False)
            elif stats_dict["roles"] == "Bronze":
                self.create_embed(0x997676, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'**Bronze** <:bronze:756094436940841049>', inline=False)
            elif stats_dict["roles"] == "Silver":
                self.create_embed(0xadadad, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'**Silver** <:silver:756094456930762799>', inline=False)
            elif stats_dict["roles"] == "Gold":
                self.create_embed(0xffbd4d, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'**Gold** <:gold:756093752707121222>', inline=False)
            elif stats_dict["roles"] == "Diamond":
                self.create_embed(0xc9f6f8, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'**Diamond** <:omega:756090831768780860>', inline=False)
            elif stats_dict["roles"] == "High Roller":
                self.create_embed(0x7e3a8a, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'**High Roller** <:omega:756090831768780860>', inline=False)
            elif stats_dict["roles"] == "Super High Roller":
                self.create_embed(0x0a8cf0, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'**Super High Roller** <:omega:756090831768780860>', inline=False)
            elif stats_dict["roles"] == "VIP":
                self.create_embed(0xff3b3b, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'**VIP** <:omega:756090831768780860>', inline=False)
            elif stats_dict["roles"] == "VVIP":
                self.create_embed(0x110d11, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'**VVIP** <:VVIP:762310707445366815>', inline=False)
            else:
                self.create_embed(0xfffff1, '' , f'{author_name}', current_member.avatar_url)
                self.embed.add_field(name="Rank", value=f'UNRANKED ', inline=False)
            self.embed.add_field(name="Total Bet", value=f'**{stats_dict["tb"]}**', inline=False)
            self.embed.add_field(name="Total Bet (Week)", value=f'**{stats_dict["tbw"]}**', inline=False)
            self.embed.add_field(name="Total Bet (Month)", value=f'**{stats_dict["tbm"]}**', inline=False)
            await ctx.send(embed=self.embed)

    #error handling for check_balance
    @check_stats.error
    async def check_stats_error(self,ctx, error):
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')


    bot = commands.Bot(command_prefix="!", case_insensitive=True)

    # this is dming users with a certain role
    @commands.command()
    @commands.guild_only()
    async def withdraw(self, ctx, amount : int): # announces to the specified role
        if amount < 50:
            embed = discord.Embed(color=0xfffff1, description='Minimum Withdrawal is 50!')
            embed.set_author(name=f'Withdrawal Request',icon_url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
            return
        self.db_conn.dbconn_open()
        userId = f'<@!{ctx.author.id}>'
        print(userId)
        if((self.db_conn.get_current_balance(userId) - amount) >= 0 ):
            role = ctx.message.guild.get_role(754825078557900870)
            for member in ctx.message.guild.members:
                if role in member.roles:
                    await member.send(f'Withdrawal Requested by {ctx.author} for {amount} {self.currency_name} @ {time.ctime()}')
        else:
            embed = discord.Embed(color=0xfffff1, description='You have insufficient balance!')
            embed.set_author(name=f'Withdrawal Request',icon_url=ctx.guild.icon_url)
            # embed.set_footer(text='You have insufficient balance!')
            await ctx.send(embed=embed)
        self.db_conn.dbconn_close()

    @withdraw.error
    # feel free to add another decorator here if you wish for it to send the same messages
    # for the same exceptions: e.g. @userinfo.error
    async def withdraw_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=0xfffff1, description='Enter the right command .withdraw <amount>' )
            embed.set_author(name=f'Withdrawal Request',icon_url=ctx.guild.icon_url)
            # embed.set_footer(text='You have insufficient balance!')
            await ctx.send(embed=embed)
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')

def setup(client):
    client.add_cog(Balance(client))
    print("Cog - \"Balance\" Loaded")
