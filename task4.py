import discord
from discord.ext import commands

# Define the intents
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print("bot online")

@bot.event
async def on_member_join(member):
    guild = bot.get_guild() # guild id
    channel = guild.get_channel() # channel id
    
    await channel.send(f"Hello {member.mention}!")
    
@bot.event
async def on_message(message):   
    if message.author.bot:
        return
     
    if message.content != "":
        await message.channel.send(f"Hello {message.author}!")

# Add the follwing permissions (68608):
#   Read Message History
#   Send Messages
#   Read Messages/View Channels
bot.run('YOUR_TOKEN_HERE')