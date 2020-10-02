import discord
import os
from cogs.db import dbconn

from discord.ext import commands

db_conn = dbconn()
# To add command prefix
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("Bot Loaded")

@client.event
async def on_member_join(member : discord.Member):
    user = f'{member}'
    userId = f'<@!{str(member.id)}>'
    db_conn.dbconn_open()
    reg_role = db_conn.register_user(user,userId)
    for role in member.guild.roles:
        if role.name == reg_role:
            reg_role = role
    await member.add_roles(reg_role)
    db_conn.dbconn_close()
    print(f'{member} : {userId} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.command() 
@commands.has_any_role('Omega')
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.has_any_role('Omega')
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

#for loading all files
client.load_extension('cogs.toss')
client.load_extension('cogs.balance')
client.load_extension('cogs.ani')
client.load_extension('cogs.blackjack')
client.load_extension('cogs.admin_u')

# run the bot using token supplied.
client.run('NzUxMTQ4ODEzMDc0NDMyMTMy.X1E32A.SDIKJYDlLJwk3OUJZdz2avkzn8U')
