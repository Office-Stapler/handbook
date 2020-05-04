import discord 
import json
from discord.ext import commands
from commands import search

with open('config.json', 'r') as f:
    config = json.load(f)
TOKEN = config['token']
BOT = commands.Bot(config['prefix'])

@BOT.event
async def on_ready():
    print('-----------------------')
    print(f'     Logged in')
    print('-----------------------')

@BOT.command(name='search')
async def search_code(ctx, subject):
    info = search.search(subject)
    if not info:
        await ctx.send('Please enter a valid course code!')
    elif isinstance(info, list):
        e = discord.Embed(
            title=f"Couldn't find {subject}, but we found courses within the faculty",
            description=str([x[0] for x in info]).replace("'", ''),
            colour=0xFFFF00
        )
        await ctx.send(embed=e)
    else:
        e = discord.Embed(
            title=f'About {subject.upper()}: {info["name"]}',
            description=info['overview'],
            colour=discord.Color(0x000ff)
        )
        e.add_field(name='Offering Terms', value=info['terms'])
        await ctx.send(embed=e)

if __name__ == "__main__":
    BOT.run(TOKEN)
