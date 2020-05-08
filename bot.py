import discord 
import json
from discord.ext import commands
from commands import search
from commands import countdown
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
            description=str(info).replace("'", ''),
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
        e.add_field(name='Conditions for Enrolment', value='None found' if info['prereq'] == [] else info['prereq'][0])
        await ctx.send(embed=e)

@BOT.command(name='results')
async def get_time(ctx):
    diff = countdown.countdown()
    if diff.days > 0:
        await ctx.send(f'There are {diff.days} days left')
if __name__ == "__main__":
    BOT.run(TOKEN)
