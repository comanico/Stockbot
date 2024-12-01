import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# If the token is not found, this will raise an exception and stop the script
if not TOKEN:
    raise ValueError("Bot token not found in environment variables.")

# Set up intents for the bot
intents = discord.Intents.default()
intents.message_content = True  # This is necessary if you want to read message content

# Initialize the bot with the command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Event handler for when the bot has successfully connected to Discord."""
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='hello')
async def hello(ctx):
    """Command that makes the bot say hello."""
    await ctx.send('Hello! I am a bot!')

@bot.event
async def on_message(message):
    """Event handler for messages. Checks if the bot was mentioned."""
    if bot.user in message.mentions:
        await message.channel.send(f'Hello, {message.author.mention}! You mentioned me.')
    await bot.process_commands(message)  # This line is crucial for commands to work

# Run the bot with the token
bot.run(TOKEN)