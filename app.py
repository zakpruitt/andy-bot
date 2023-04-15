import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!tmb ", intents=intents)


async def load_extensions():
    for file in os.listdir(os.getenv("PATH") + "modules/cogs"):
        if file.startswith("__pycache__"):
            continue
        await client.load_extension(f"modules.cogs.{file[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start(os.getenv("TOKEN"))


asyncio.run(main())
