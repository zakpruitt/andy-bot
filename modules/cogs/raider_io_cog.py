import traceback

import discord
from discord.ext import commands
from discord import app_commands

from modules.services.raider_io_service import RaiderIoService


class RaiderIoCog(commands.Cog, name="Raider IO"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="get_io_history", description="Displays a player's raider.io history in an embed.")
    async def get_io_history(self, interaction: discord.Interaction, name: str, realm: str, region: str = 'us'):
        try:
            await interaction.response.send_message(f"Retrieving {name}'s Raider.IO history...",
                                                    ephemeral=True)
            embed = RaiderIoService.get_raider_io_history(name, realm, region)
            await interaction.channel.send(embed=embed.get_embed())
        except Exception as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
            await interaction.channel.send(embed=embed.error())


async def setup(bot: commands.Bot):
    await bot.add_cog(RaiderIoCog(bot))
