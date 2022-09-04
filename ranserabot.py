import os
from dotenv import load_dotenv
import discord
from discord.utils import get

#---------------
load_dotenv()
TOKEN = os.getenv("TOKEN")

servers=[957056381154918461,747312626605883423]
intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)
#-----
#Login Message
@bot.event
async def on_ready():
  print(f"We have logged in as {bot.user}")

#On User Join
@bot.event
async def on_member_join(member):
  role = get(member.guild.roles, name="Vibin")
  await member.add_roles(role)
  await member.send(f'Welcome {member.name}, to Ransera!')

#---------------
#Test Command
@bot.slash_command(guild_ids=servers)
async def hello(ctx):
  await ctx.respond("Hello!")

#Copy Command
@bot.slash_command(guild_ids=servers)
async def copy(ctx,*,arg):
  await ctx.send(arg)
#---------------

# PC cog has the PC directory/lookup commands.
# Info cog has the old info command as well as other utility commands, such as season, pronouns, and wiki lookup.
# Fun cog has fortunetelling, quotes, tic-tac-toe
# Future Gen cog will have the random gen commands, or it may be folded into fun.

#---------------
cogs_list = [
    'pc',
    'util',
    'fun'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')
#---------------
bot.run(TOKEN)
