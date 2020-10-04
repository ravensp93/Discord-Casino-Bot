import discord
import random
from discord.ext import commands
from cogs.db import dbconn
from cogs.deckArt import deckArt
import asyncio

class Ani(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db_conn = dbconn()
        self.currency_name = "ZEN"
        self.count = 0
        self.deck = ["D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","DJ","DQ","DK"\
                    ,"C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","CJ","CQ","CK"\
                    ,"H1","H2","H3","H4","H5","H6","H7","H8","H9","H10","HJ","HQ","HK"\
                    ,"S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","SJ","SQ","SK"
                    ]


    @commands.command()
    @commands.guild_only()
    async def ani(self,ctx):
        print("test")

def setup(client):
    client.add_cog(Ani(client))
    print("Cog - \"Ani\" Loaded")
