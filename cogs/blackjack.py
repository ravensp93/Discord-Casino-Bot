import discord
import random
from discord.ext import commands
from cogs.db import dbconn
from cogs.deckArt import deckArt
import asyncio

class Blackjack(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.currency_name = "ZEN"
        self.channel_lock = []


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

    @commands.cooldown(rate=1, per=2)
    @commands.command(name="bj")
    @commands.guild_only()
    async def blackjack(self, ctx, amount:int, pp_amount = 0):
        db_conn = dbconn()
        db_conn.dbconn_open()
        if ctx.message.channel.name == "blackjack-2" or ctx.message.channel.name == "blackjack-1":
            if ctx.message.channel not in self.channel_lock:
                channel = ctx.message.channel
                userId = f'<@!{ctx.author.id}>'
                current_member = await ctx.guild.fetch_member(ctx.author.id)
                if db_conn.get_current_balance(userId) >= (amount+pp_amount):
                    #Check Minimum bet
                    if amount < 1:
                        embed = discord.Embed(color=0xfffff1, description=f'**Minimum Bet is 1 {self.currency_name}!**')
                        embed.set_author(name=f'Blackjack',icon_url=ctx.guild.icon_url)
                        await ctx.send(embed=embed)
                        db_conn.dbconn_close()
                        return

                    #Game code
                    #Reset
                    deck = ["DA","D2","D3","D4","D5","D6","D7","D8","D9","D10","DJ","DQ","DK"\
                            ,"CA","C2","C3","C4","C5","C6","C7","C8","C9","C10","CJ","CQ","CK"\
                            ,"HA","H2","H3","H4","H5","H6","H7","H8","H9","H10","HJ","HQ","HK"\
                            ,"SA","S2","S3","S4","S5","S6","S7","S8","S9","S10","SJ","SQ","SK"
                            ]*4

                    black_suit = ["C","S"]
                    red_suit = ["H","D"]
                    dealer_hand = ''
                    player_hand = ''
                    raw_player_hand = []
                    raw_dealer_hand = []
                    pp_hand = []
                    dealer_score = 0
                    player_score = 0
                    game_over = 0
                    game_start = True
                    pp_payout = 0
                    total_payout = 0
                    pp_payout_type = "None"
                    blackjack = False

                    embed = discord.Embed(color=0xffA1f1)
                    embed.set_author(name=f'{current_member.name}',icon_url=current_member.avatar_url)
                    embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\nPerfect Pair: {pp_amount} {self.currency_name}\n Please type **hit** or **stand**',inline=False)


                    def calc_score(dealer):
                        total_score = 0
                        if dealer:
                            hand = raw_dealer_hand
                        else:
                            hand = raw_player_hand
                        for x in range(2):
                            for card in hand:
                                if x == 0 and card[1:] == "A":
                                    continue
                                elif x == 1 and card[1:] != "A":
                                    continue
                                else:
                                    if card[1:] == "A":
                                        if total_score <= 10:
                                            total_score = total_score + 11
                                        else:
                                            total_score = total_score + 1
                                    elif card[1:] == "J" or  card[1:] == "Q" or card[1:] == "K":
                                        total_score = total_score + 10
                                    else:
                                        total_score = total_score + int(card[1:])
                        #assign hand and score
                        return total_score

                    def deal_card(dealer, dealer_score, player_score, player_hand, dealer_hand):
                        draw = random.randint(0, len(deck))
                        card = deck.pop(draw)

                        if dealer:
                            raw_dealer_hand.append(card)
                            if len(pp_hand) < 2:
                                pp_hand.append(card)
                            dealer_hand = dealer_hand + deckArt.deck[card]
                            return calc_score(True),dealer_hand
                        else:
                            raw_player_hand.append(card)
                            if len(pp_hand) < 2:
                                pp_hand.append(card)    
                            player_hand = player_hand + deckArt.deck[card]
                            return calc_score(False),player_hand

                    dealer_score,dealer_hand = deal_card(True, dealer_score, player_score, player_hand, dealer_hand)
                    player_score,player_hand = deal_card(False, dealer_score, player_score, player_hand, dealer_hand)
                    player_score,player_hand = deal_card(False, dealer_score, player_score, player_hand, dealer_hand)

                    if pp_hand[0][1:] == pp_hand[1][1:]:
                        if pp_hand[0][:-1] == pp_hand[1][:-1]:
                            pp_payout_type = "Perfect Pair"
                            pp_payout = pp_amount * 25
                        elif (pp_hand[0][:-1] in black_suit and pp_hand[1][:-1] in black_suit) or (pp_hand[0][:-1] in red_suit and pp_hand[1][:-1] in red_suit):
                            pp_payout_type = "Colored Pair"
                            pp_payout = pp_amount * 12
                        else:
                            pp_payout_type = "Mixed Pair"
                            pp_payout = pp_amount * 6


                    if player_score == 21:
                        blackjack = True


                    while not game_over and blackjack == False:
                        if game_start:
                            embed.add_field(name=f'Player\'s Hand ({player_score})', value=player_hand,inline=False)
                            embed.add_field(name=f'Dealers\'s Hand ({dealer_score})', value=dealer_hand,inline=False)
                            # self.channel_lock.append(ctx.message.channel)
                            game_msg = await channel.send(embed=embed)
                            game_start = False
                        def check(m):
                            return (str.lower(m.content) == 'hit' or  str.lower(m.content) == 'stand') and m.channel == channel and m.author == ctx.author

                        try:
                            msg = await self.client.wait_for('message', timeout=20.0, check=check)
                            
                        except asyncio.TimeoutError:
                            game_over = 1
                        else:
                            if str.lower(msg.content) == "hit":
                                player_score, player_hand = deal_card(False, dealer_score, player_score, player_hand, dealer_hand)
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
                                    dealer_score,dealer_hand = deal_card(True, dealer_score, player_score, player_hand, dealer_hand)
                        # # if(self.db_conn.withdraw_bal(userId, amount)):
                        #     self.db_conn.update_lad_bet(userId, amount)
                        #     self.db_conn.deposit_bal(userId, int(amount * 1.9))
                        #     self.db_conn.dbconn_close()
                    if player_score <= 21:
                        if dealer_score <= 21:
                            if player_score > dealer_score:
                                total_payout = amount*2 + pp_payout
                                embed = discord.Embed(color=0x32CD32)
                                embed.set_author(name=f'{current_member.name}',icon_url=current_member.avatar_url)
                                embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\nPerfect Pair: {pp_amount} {self.currency_name}**({pp_payout_type})**\n Payout: {total_payout} {self.currency_name}',inline=False)
                            elif dealer_score > player_score:
                                total_payout = pp_payout
                                embed = discord.Embed(color=0xFF0000)
                                embed.set_author(name=f'{current_member.name}',icon_url=current_member.avatar_url)
                                embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\nPerfect Pair: {pp_amount} {self.currency_name}**({pp_payout_type})**\n Payout: {total_payout} {self.currency_name}',inline=False)                    
                            else:
                                total_payout = amount + pp_payout
                                embed = discord.Embed(color=0xFFA500)
                                embed.set_author(name=f'{current_member.name}',icon_url=current_member.avatar_url)
                                embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\nPerfect Pair: {pp_amount} {self.currency_name}**({pp_payout_type})**\n Payout: {total_payout} {self.currency_name}',inline=False)
                        else:
                            total_payout = amount*2 + pp_payout
                            embed = discord.Embed(color=0x32CD32)
                            embed.set_author(name=f'{current_member.name}',icon_url=current_member.avatar_url)
                            embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\nPerfect Pair: {pp_amount} {self.currency_name}**({pp_payout_type})**\n Payout: {total_payout} {self.currency_name}',inline=False)
                    else:
                        total_payout = pp_payout
                        embed = discord.Embed(color=0xFF0000)
                        embed.set_author(name=f'{current_member.name}',icon_url=current_member.avatar_url)
                        embed.add_field(name="Blackjack", value=f'Wager: {amount} {self.currency_name}\nPerfect Pair: {pp_amount} {self.currency_name}**({pp_payout_type})**\n Payout: {total_payout} {self.currency_name}',inline=False)    
                    
                    embed.add_field(name=f'Player\'s Hand ({player_score})', value=player_hand,inline=False)
                    embed.add_field(name=f'Dealers\'s Hand ({dealer_score})', value=dealer_hand,inline=False)
                    if blackjack:
                        embed.set_field_at(1, name=f'Player\'s Hand <:sanc:762681431645487114>', value=player_hand,inline=False)
                        await channel.send(embed=embed)
                    else:
                        await game_msg.edit(embed=embed)
                    #end
                    db_conn.withdraw_bal(userId, amount+pp_amount)
                    if(total_payout != 0):
                        db_conn.deposit_bal(userId, total_payout)
                    db_conn.update_lad_bet(userId, amount+pp_amount)
                    self.channel_lock.remove(ctx.message.channel)
                else:
                    embed = discord.Embed(color=0xfffff1, description=f'**You have insufficient balance!**')
                    embed.set_author(name=f'{current_member.name}',icon_url=current_member.avatar_url)
                    await ctx.send(embed=embed)
            else:
                await ctx.send("The current **Blackjack** game is not over")
        else:
            await ctx.send("Please head over to the blackjack channel!")
        db_conn.dbconn_close()

    #error handling for blackjack
    @blackjack.error
    async def blacjack_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=0xfffff1, description='Enter the right command - .bj <amount>')
            embed.set_author(name=f'Blackjack',icon_url=ctx.guild.icon_url)
            # embed.set_footer(text='You have insufficient balance!')
            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("This command is on cooldown")
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')

def setup(client):
    client.add_cog(Blackjack(client))
    print("Cog - \"Blackjack\" Loaded")
