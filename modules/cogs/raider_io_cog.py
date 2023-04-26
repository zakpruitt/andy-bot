import os
import traceback

from discord.ext import commands

from modules.services.droptimizer_service import DroptimizerService
from modules.services.raider_io_service import RaiderIoService
from modules.utilities.google_sheets_utility import GoogleSheetsUtility


class RaiderIoCog(commands.Cog, name="Raider IO"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command('riohistory')
    async def get_io_history(self, ctx: commands.Context, name: str, realm: str, region: str = 'us'):
        """ Displays a player's raider.io history. """
        msg = await ctx.send(f"Retrieving {name}'s Raider.IO history...")
        embed = RaiderIoService.get_raider_io_history(name, realm, region)
        await msg.edit(content="", embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(RaiderIoCog(bot))
