import discord
import random
from discord.ext import commands
from cogs.db import dbconn
import asyncio

class Blackjack(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db_conn = dbconn()
        self.currency_name = "ZEN"
        self.user_lock = []


    # #View Module
    # def create_embed(self, player_icon, name, amount, player_hand=None, dealer_hand=None, win=None, player_score=0, dealer_score=0, payout=0):

    #     if win is None:
    #         embed = discord.Embed(color=0xffA1f1)
    #         embed.set_author(name=name,icon_url=player_icon)
    #         embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Please type **hit** or **stand**',inline=False)
    #     else:
    #         if win == 1:
    #             embed = discord.Embed(color=0x32CD32)
    #             embed.set_author(name=name,icon_url=player_icon)
    #             embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Payout: {amount*2} {self.currency_name}',inline=False)
    #         elif win == 2:
    #             embed = discord.Embed(color=0xFF0000)
    #             embed.set_author(name=name,icon_url=player_icon)
    #             embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Payout: 0 {self.currency_name}',inline=False)
    #         elif win == 3:
    #             embed = discord.Embed(color=0xFF0000)
    #             embed.set_author(name=name,icon_url=player_icon)
    #             embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Payout: {amount} {self.currency_name}',inline=False)
    #     embed.add_field(name=f'Player\'s Hand ({player_score})', value=player_hand,inline=False)
    #     embed.add_field(name=f'Dealers\'s Hand ({dealer_score})', value=dealer_hand,inline=False)
    #     return embed 

    @commands.command(name="bj")
    @commands.guild_only()
    async def blackjack(self, ctx, amount:int):
        if ctx.author not in self.user_lock:

            #INFO PACK
            self.user_lock.append(ctx.author)
            #retrieve guild object
            self.guild = await self.client.fetch_guild(self.client.guilds[0].id)
            #retrieve member obj using guild obj
            current_member = await self.guild.fetch_member(ctx.author.id)
            #retrieve name using member obj
            name = current_member.name
            #start
            # self.db_conn.dbconn_open()
            userId = f'<@!{ctx.author.id}>'


            if amount < 1:
                embed = discord.Embed(color=0xfffff1, description=f'**Minimum Bet is 1 {self.currency_name}!**')
                embed.set_author(name=f'Blackjack',icon_url=ctx.guild.icon_url)
                await ctx.send(embed=embed)
                return

            #Game code
            #Reset
            deck = ["DA","D2","D3","D4","D5","D6","D7","D8","D9","D10","DJ","DQ","DK"\
                    ,"CA","C2","C3","C4","C5","C6","C7","C8","C9","C10","CJ","CQ","CK"\
                    ,"HA","H2","H3","H4","H5","H6","H7","H8","H9","H10","HJ","HQ","HK"\
                    ,"SA","S2","S3","S4","S5","S6","S7","S8","S9","S10","SJ","SQ","SK"
                    ]

            dealer_hand = []
            player_hand = []
            dealer_score = 0
            player_score = 0
            game_over = 0
            game_start = True

            embed = discord.Embed(color=0xffA1f1)
            embed.set_author(name=name,icon_url=current_member.avatar_url)
            embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Please type **hit** or **stand**',inline=False)


            def deal_card(dealer, dealer_score, player_score):
                card_val = 0
                draw = random.randint(0, len(deck))
                card = deck.pop(draw)
                #assign card value
                if card[1:] == "A":
                    card_val = 1
                    if dealer:
                        if len(dealer_score) <= 10:
                            card_val = 11
                    else:
                        if len(player_score) <= 10:
                            card_val = 11
                elif card[1:] == "J" or  card[1:] == "Q" or card[1:] == "K":
                    card_val = 10
                else:
                    card_val = int(card[1:])
                #assign hand and score
                if dealer:
                    dealer_hand.append(card)
                    dealer_score = dealer_score + card_val
                    return dealer_score
                else:
                    player_hand.append(card)
                    player_score = player_score + card_val
                    return player_score

            dealer_score = deal_card(True, dealer_score, player_score)
            player_score = deal_card(False, dealer_score, player_score)
            dealer_score = deal_card(True, dealer_score, player_score)
            player_score = deal_card(False, dealer_score, player_score)

            while not game_over:
                channel = ctx.message.channel
                if game_start:
                    print("test")
                    embed.add_field(name=f'Player\'s Hand ({player_score})', value=player_hand,inline=False)
                    embed.add_field(name=f'Dealers\'s Hand ({dealer_score})', value=dealer_hand,inline=False)
                    game_msg = await channel.send(embed=embed)
                    game_start = False
                def check(m):
                    return (str.lower(m.content) == 'hit' or  str.lower(m.content) == 'stand') and m.channel == channel and m.author == ctx.author

                try:
                    msg = await self.client.wait_for('message', timeout=20.0, check=check)
                except asyncio.TimeoutError:
                    await channel.send('Timeout...man')
                    game_over = 1
                else:
                    if str.lower(msg.content) == "hit":
                        player_score = deal_card(False, dealer_score, player_score)
                        embed.set_field_at(1, name=f'Player\'s Hand ({player_score})', value=player_hand,inline=False)
                        embed.set_field_at(2, name=f'Dealers\'s Hand ({dealer_score})', value=dealer_hand,inline=False)
                        await game_msg.edit(embed=embed)
                        if player_score >= 21 :
                            game_over = 1
                    elif str.lower(msg.content) == "stand":
                        print("stand")
                        game_over = 1
                if game_over:
                    if player_score <= 21:
                        while dealer_score < 17:
                            dealer_score = deal_card(True, dealer_score, player_score)
                # # if(self.db_conn.withdraw_bal(userId, amount)):
                #     self.db_conn.update_lad_bet(userId, amount)
                #     self.db_conn.deposit_bal(userId, int(amount * 1.9))
                #     self.db_conn.dbconn_close()
            if player_score <= 21:
                if dealer_score <= 21:
                    if player_score > dealer_score:
                        embed = discord.Embed(color=0x32CD32)
                        embed.set_author(name=name,icon_url=current_member.avatar_url)
                        embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Payout: {amount*2} {self.currency_name}',inline=False)
                    elif dealer_score > player_score:
                        embed = discord.Embed(color=0xFF0000)
                        embed.set_author(name=name,icon_url=current_member.avatar_url)
                        embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Payout: 0 {self.currency_name}',inline=False)                    
                    else:
                        embed = discord.Embed(color=0xFFA500)
                        embed.set_author(name=name,icon_url=current_member.avatar_url)
                        embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Payout: {amount} {self.currency_name}',inline=False)
                else:
                    embed = discord.Embed(color=0x32CD32)
                    embed.set_author(name=name,icon_url=current_member.avatar_url)
                    embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Payout: {amount*2} {self.currency_name}',inline=False)
            else:
                embed = discord.Embed(color=0xFF0000)
                embed.set_author(name=name,icon_url=current_member.avatar_url)
                embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\n Payout: 0 {self.currency_name}',inline=False)    
            embed.add_field(name=f'Player\'s Hand ({player_score})', value=player_hand,inline=False)
            embed.add_field(name=f'Dealers\'s Hand ({dealer_score})', value=dealer_hand,inline=False)
            await game_msg.edit(embed=embed)
            #end
            self.user_lock.remove(ctx.author)
        else:
            await ctx.send("Your current **Blackjack** game is not over")

    #error handling for blackjack
    @blackjack.error
    async def blacjack_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=0xfffff1, description='Enter the right command - .bj <amount>')
            embed.set_author(name=f'Blackjack',icon_url=ctx.guild.icon_url)
            # embed.set_footer(text='You have insufficient balance!')
            await ctx.send(embed=embed)
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')

def setup(client):
    client.add_cog(Blackjack(client))
    print("Cog - \"Blackjack\" Loaded")
