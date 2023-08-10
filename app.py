import asyncio
import logging
import os
import platform
import time

import discord
from colorama import Back, Fore, Style
from discord.app_commands import MissingAnyRole
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or("!aa "), intents=intents)


async def load_extensions():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cogs_dir = os.path.join(base_dir, "modules", "cogs")

    for file in os.listdir(cogs_dir):
        if file.startswith("__pycache__"):
            continue
        await client.load_extension(f"modules.cogs.{file[:-3]}")


@client.event
async def on_app_command_error(interaction, error):
    if isinstance(error, MissingAnyRole):
        await interaction.followup.send("You do not have permission to run this command.")


@client.event
async def on_ready():
    prefix = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC",
                                                      time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prefix + " Logged in as " + Fore.YELLOW + client.user.name)
    print(prefix + " Bot ID " + Fore.YELLOW + str(client.user.id))
    print(prefix + " Discord Version " + Fore.YELLOW + discord.__version__)
    print(prefix + " Python Version " + Fore.YELLOW + str(platform.python_version()))
    synced = await client.tree.sync()
    print(prefix + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")


async def main():
    async with client:
        await load_extensions()
        await client.start(os.getenv("TOKEN"))


asyncio.run(main())
