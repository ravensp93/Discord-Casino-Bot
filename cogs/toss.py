import discord
import random
from discord.ext import commands
from cogs.db import dbconn
import asyncio

class Toss(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db_conn = dbconn()
        self.currency_name = "ZEN"
        self.user_lock = []

    @commands.command()
    @commands.guild_only()
    async def toss(self, ctx, amount:int):
        if ctx.author not in self.user_lock:

            #INFO PACK
            self.user_lock.append(ctx.author)
            #retrieve guild object
            guild = await self.client.fetch_guild(self.client.guilds[0].id)
            #retrieve member obj using guild obj
            current_member = await guild.fetch_member(ctx.author.id)
            #retrieve name using member obj
            name = current_member.name
            #check min amount
            if amount < 10:
                embed = discord.Embed(color=0xfffff1, description=f'**Minimum Bet is 10 {self.currency_name}!**')
                embed.set_author(name=f'Coin Toss',icon_url=ctx.guild.icon_url)
                await ctx.send(embed=embed)
                return

            self.db_conn.dbconn_open()
            userId = f'<@!{ctx.author.id}>'

            if(self.db_conn.withdraw_bal(userId, amount)):
                self.db_conn.update_lad_bet(userId, amount)
                flip_result = self.coinflip()
                name = current_member.name
                #win
                if flip_result == 1:
                    self.db_conn.deposit_bal(userId, int(amount * 1.9))
                    embed = discord.Embed(color=0x32CD32)
                    embed.set_author(name=f'{name}',icon_url=current_member.avatar_url)
                    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/754786420568096979/754811702368927764/icon.png')
                    embed.add_field(name="Coin Toss", value=f'Results: The coin lands on.... **Heads**!\nWager: **{amount} {self.currency_name}** - Payout {int(amount*1.9)} {self.currency_name}',inline=False)
                    await ctx.send(embed=embed)
                #lose
                else:
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_author(name=f'{name}',icon_url=current_member.avatar_url)
                    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/754786420568096979/754813613214007386/icon2.png')
                    embed.add_field(name="Coin Toss", value=f'Results: The coin lands on.... **Tails**!\nWager: **{amount} {self.currency_name}** - Payout 0 {self.currency_name}',inline=False)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=0xfffff1, description='You have insufficient balance!')
                embed.set_author(name=f'{name}',icon_url=current_member.avatar_url)
                # embed.set_footer(text='You have insufficient balance!')
                await ctx.send(embed=embed)
                self.db_conn.dbconn_close()
            self.user_lock.remove(ctx.author)
        else:
            await ctx.send("Your current **Toss** game is not over")

    #error handling for toss
    @toss.error
    async def toss_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=0xfffff1, description='Enter the right command - .toss <amount>')
            embed.set_author(name=f'Coin Toss',icon_url=ctx.guild.icon_url)
            # embed.set_footer(text='You have insufficient balance!')
            await ctx.send(embed=embed)
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')

    def coinflip(self):
        return random.randint(0, 1)

def setup(client):
    client.add_cog(Toss(client))
    print("Cog - \"Toss\" Loaded")
