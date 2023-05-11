import os
import traceback

import discord
from discord import app_commands
from discord.app_commands import MissingAnyRole
from discord.ext import commands

from modules.services.droptimizer_service import DroptimizerService
from modules.utilities.google_sheets_utility import GoogleSheetsUtility


class DroptimizerCog(commands.Cog, name="Droptimizer"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.DROPTIMIZER_CHANNEL_ID = int(os.getenv("DROPTIMIZER_CHANNEL_ID"))
        self.sheets_util = GoogleSheetsUtility(os.getenv('DROPTIMIZER_SPREADSHEET_NAME'))

    @app_commands.command(name="droptimizer_run", description="Parses all input droptimizer links.")
    @commands.has_any_role('Officer', 'Recruiter')
    async def run_droptimizer_reports(self, interaction: discord.Interaction):
        try:
            progress_embed = DroptimizerService.get_progress_embed()
            progress_msg = await interaction.channel.send(embed=progress_embed.get_embed())
            await interaction.response.send_message('Droptimizer report processing started!',
                                                    ephemeral=True)
            await DroptimizerService.process_droptimizer_reports(progress_embed, progress_msg)
        except MissingAnyRole as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
        except Exception as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
            await progress_msg.edit(embed=progress_embed.error(), delete_after=30)

    @app_commands.command(name='droptimizer_query', description='Queries droptimizer data and displays it in an embed.')
    @commands.has_any_role('Officer', 'Recruiter')
    async def search_droptimizer_data(self, interaction: discord.Interaction, difficulty: str, boss_or_item: str,
                                      query: str, mobile_friendly: str = ""):
        # Defer the response
        await interaction.response.defer()

        # Check parameters for validity
        if difficulty.lower() not in ['mythic', 'heroic', 'normal']:
            await interaction.response.send_message('Invalid difficulty. Valid options: Mythic, Heroic, and Normal',
                                                    ephemeral=True)
            return
        if boss_or_item.lower() not in ['boss', 'item']:
            await interaction.response.send_message('Invalid type. Valid options: Boss, Item',
                                                    ephemeral=True)
            return

        searching_message = await interaction.followup.send('Searching...', ephemeral=True)
        try:
            search_embed = DroptimizerService.search_droptimizer_data(difficulty.capitalize(), boss_or_item.lower(),
                                                                      query)
            if mobile_friendly.lower() == "mf":
                await searching_message.edit(content='', embed=search_embed.get_mobile_friendly_embed())
            else:
                await searching_message.edit(content='', embed=search_embed.get_embed())
        except MissingAnyRole as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
        except Exception as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
            await searching_message.delete()
            await interaction.followup.send(
                f"I couldn't find any results found for {query}. Please check your query and try again. 🫂",
                ephemeral=True)

    @app_commands.command(name='droptimizer_catchup',
                          description='Retrieves links in the instance the bot was offline.')
    @commands.has_any_role('Officer', 'Recruiter')
    async def catchup_droptimizer_links(self, interaction: discord.Interaction):
        if interaction.channel.id != self.DROPTIMIZER_CHANNEL_ID:
            return

        await interaction.response.defer()

        try:
            async for message in interaction.channel.history(limit=None, oldest_first=True):
                if message.author.id == self.bot.user.id:
                    await message.delete()
                    continue
                await self.on_message(message)
            interaction.followup.send(f"All reports caught up! <:tier5:1085390493778710683>",
                                      ephemeral=True)
        except MissingAnyRole as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
        except Exception as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
            await interaction.followup.send(
                f"Error catching up! Please review logs and try again later.",
                ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """ Listens for droptimizer links and appends them to the spreadsheet. """
        if message.channel.id != self.DROPTIMIZER_CHANNEL_ID:
            return

        mention = message.author.mention
        try:
            if 'https://www.raidbots.com/simbot/report' in message.content:
                links_processed = await DroptimizerService.add_droptimizer_report(message.content)
                await message.delete()
                await message.channel.send(
                    f"I successfully processed {links_processed} link(s). Thank you, {mention}! <:tier5:1085390493778710683>",
                    delete_after=10800)
        except Exception as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
            await message.reply(f"There was an error processing your droptimizer report(s), {mention}. "
                                f"<:TrollDespair:1081251201951223819>\n\nPlease verify your link(s) are correct"
                                f"! If your link(s) are valid and issues persist, please ping an "
                                f"officer. <:Okayge:1103488695174189177> 👍",
                                delete_after=10800)


async def setup(bot: commands.Bot):
    await bot.add_cog(DroptimizerCog(bot))
