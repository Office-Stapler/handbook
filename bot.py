import discord 
import json
from discord.ext import commands
from commands import code
from commands import search
from commands import timetable

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

@BOT.command(name='timetable')
async def find_times(ctx, *courseperiod):
    try:
        period = courseperiod[1].upper()
        subject = courseperiod[0].upper()
        times = timetable.timetable(subject)
    except:
        await ctx.send('Invalid format, please do coursecode period. E.g: COMP2511 T3')
        return
    info = times[period]
    if not info:
        await ctx.send(f"Course code is wrong or the course doesn't run in {period}")
        return
    types = [
    'Activity',	
    'Period',
    'Class',
    'Section Status',
    'Enrols/Capacity',
	'Day/Start Time'
    ]
    e = discord.Embed(
        title=f'About {subject} in {period}',
        url=f'http://timetable.unsw.edu.au/2020/{subject.upper()}.html#S{period[1]}'
    )
    for time in info:
        if len(types) == len(time):
            e.add_field(
                name = time[0],
                value = f'{time[5]}\nStatus: {time[3]}'
            )
    await ctx.send(embed=e)

if __name__ == "__main__":
    BOT.run(TOKEN)
