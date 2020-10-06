import discord
import random
from discord.ext import commands
from cogs.db import dbconn
from cogs.deckArt import deckArt
import asyncio
from cogs.rwcsv import rwcsv

class CSP(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.currency_name = "ZEN"
        self.channel_lock = []



    @commands.cooldown(rate=1, per=2)
    @commands.command(name="csp")
    @commands.guild_only()
    async def carribean_stud_poker(self, ctx, amount:int):



        if ctx.message.channel.name == "stud-poker-2" or ctx.message.channel.name == "stud-poker-1":
            channel = ctx.message.channel
            userId = f'<@!{ctx.author.id}>'
            current_member = await ctx.guild.fetch_member(ctx.author.id)

            black_suit = ["C","S"]
            red_suit = ["H","D"]
            dealer_hand = ''
            player_hand = ''
            raw_player_hand = []
            raw_dealer_hand = []

            deck = ["DA","D2","D3","D4","D5","D6","D7","D8","D9","D10","DJ","DQ","DK"\
            ,"CA","C2","C3","C4","C5","C6","C7","C8","C9","C10","CJ","CQ","CK"\
            ,"HA","H2","H3","H4","H5","H6","H7","H8","H9","H10","HJ","HQ","HK"\
            ,"SA","S2","S3","S4","S5","S6","S7","S8","S9","S10","SJ","SQ","SK"
            ]


            def deal_card(dealer, player_hand, dealer_hand):
                draw = random.randint(0, len(deck))
                card = deck.pop(draw)
                hand = ""

                if dealer:
                    raw_dealer_hand.append(card)
                    hand = dealer_hand + deckArt.deck[card]
                else:
                    raw_player_hand.append(card)  
                    hand = player_hand + deckArt.deck[card]
                return hand

            dealer_hand = deal_card(True, player_hand, dealer_hand)
            player_hand = deal_card(False, player_hand, dealer_hand)
            player_hand = deal_card(False, player_hand, dealer_hand)
            player_hand = deal_card(False, player_hand, dealer_hand)
            player_hand = deal_card(False, player_hand, dealer_hand)
            player_hand = deal_card(False, player_hand, dealer_hand)

            embed = discord.Embed(color=0xffA1f1)
            embed.set_author(name=f'{current_member.name}',icon_url=current_member.avatar_url)
            embed.add_field(name="Blackjack", value=f'Ante: {amount} {self.currency_name}\nCall: 0 {self.currency_name}\n Please type **Call** or **Fold**',inline=False)
        
            embed.add_field(name=f'Player\'s Hand (<Combination>)', value=player_hand,inline=False)
            embed.add_field(name=f'Dealers\'s Hand (<Combination>)', value=dealer_hand,inline=False)
            game_msg = await channel.send(embed=embed)
        else:
            await ctx.send("Please head over to the Stud Poker channel!")    

    #error handling for CSP
    @carribean_stud_poker.error
    async def blacjack_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=0xfffff1, description='Enter the right command - .csp <amount>')
            embed.set_author(name=f'Carribean Stud Poker',icon_url=ctx.guild.icon_url)
            # embed.set_footer(text='You have insufficient balance!')
            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("This command is on cooldown")
        userId = f'<@!{ctx.author.id}>'
        if isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(f'{userId} This command cannot be used in private messages')
def setup(client):
    client.add_cog(CSP(client))
    print("Cog - \"Caribbean Stud Poker\" Loaded")
