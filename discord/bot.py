import os
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
from subprocess import run,TimeoutExpired

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

def send_message(message, webhook_url):
    """Function to send a message to a channel."""
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Failed to send message: {response.text}")
    
@bot.command(name='check')
async def check(ctx, ticker):
    await ctx.send(f'Checking stock price for {ticker}...')
    investoBot = "/usr/bin/cat /d/Git/StockBot/public/AAPL.json"
    try:
        output = run(f"{investoBot}",capture_output=True, text=True, timeout=10)
        if output.returncode == 0:
            await ctx.send(f"Stock price for {ticker} is {output.stdout}")
        else:
            await ctx.send(f"Failed to check stock price for {ticker}")
    except Exception as e:
        await ctx.send(f"Failed to check stock price for {ticker}: {e}")
    except TimeoutExpired:
        await ctx.send(f"Timed out while checking stock price for {ticker}")

@bot.event
async def on_message(message):
    """Event handler for messages. Checks if the bot was mentioned."""
    if bot.user in message.mentions:
        await message.channel.send(f'Hello, {message.author.mention}! You mentioned me.')
    await bot.process_commands(message)  # This line is crucial for commands to work

# Run the bot with the token
def run_bot():
    bot.run(TOKEN)

if __name__ == '__main__':
    run_bot()