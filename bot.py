import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import logging
from colorama import Fore, Style, init

init(autoreset=True)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger('bot')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(
        f'{Fore.GREEN}[ONLINE]{Style.RESET_ALL} Logged in as {Fore.CYAN}{bot.user.name}{Style.RESET_ALL} (ID: {bot.user.id})')
    print(f'{Fore.YELLOW}[INFO]{Style.RESET_ALL} Sassy TinyLlama loaded and ready to chat!')

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="your problems (and judging)"
    ))

    await load_cogs()


async def load_cogs():
    """Load all cogs from the cogs folder"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'{Fore.BLUE}[COGS]{Style.RESET_ALL} Loaded extension: {filename}')
            except Exception as e:
                print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to load extension {filename}: {e}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if bot.user.mentioned_in(message) and not message.mention_everyone:

        content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        if content:
            async with message.channel.typing():
                cog = bot.get_cog('AIChat')
                if cog:
                    await cog.handle_chat(message, content)


@bot.command(name='reload')
@commands.is_owner()
async def reload_cogs(ctx):
    """Reload all cogs (owner only)"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.reload_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                await ctx.send(f'Error reloading {filename}: {e}')
                continue

    await ctx.send('All cogs reloaded successfully!')

if __name__ == '__main__':
    if TOKEN is None:
        print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} DISCORD_TOKEN not found in .env file')
        exit(1)

    asyncio.run(bot.start(TOKEN))