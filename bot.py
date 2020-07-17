import discord 
import json
from discord.ext import commands
from commands import code
from commands import countdown
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

@BOT.command(name='code')
async def search_code(ctx, subject):
    info = code.search(subject)
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
            description=info['overview'][:2048],
            colour=discord.Color(0x000ff),
            url=info['url']
        )
        e.add_field(name='Offering Terms', value=info['terms'], inline=False)
        e.add_field(name='Conditions for Enrolment', value='None' if info['prereq'] == [] else info['prereq'], inline=False)
        await ctx.send(embed=e)

@BOT.command(name='search')
async def serach_name(ctx, subject):
    info = search.name_search(subject)
    if not info:
        await ctx.send(f'No courses were found with the name {subject}')
    else:
        e = discord.Embed(
            title=f'List of subjects with {subject.capitalize()}',
            colour=discord.Color(0x000ff),
        )
        for subject in info:
            e.add_field(name=subject['name'], value=subject['code'])
        try:
            await ctx.send(embed=e)
        except discord.HTTPException:
            await ctx.send('Your search was too vague, please be more specific')
if __name__ == "__main__":
    BOT.run(TOKEN)
