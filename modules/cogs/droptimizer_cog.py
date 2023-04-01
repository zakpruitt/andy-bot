import os
import traceback

from discord.ext import commands

from modules.services.droptimizer_service import DroptimizerService
from modules.utilities.google_sheets_utility import GoogleSheetsUtility


class DroptimizerCog(commands.Cog, name="Droptimizer"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sheets_util = GoogleSheetsUtility(os.getenv('DROPTIMIZER_SPREADSHEET_NAME'))

    # @commands.command(name="droptimizer_run")
    # async def run_droptimizer_reports(self, ctx: commands.Context):
    #     """ Parses all input Droptimizer Links. """
    #     try:
    #         # make this into a specific embed
    #         progress_embed = DroptimizerService.get_progress_embed()
    #         progress_msg = await ctx.send(embed=progress_embed.get_embed())
    #         await DroptimizerService.process_droptimizer_reports(progress_embed, progress_msg)
    #     except Exception as e:
    #         error = str(e) + "\n\n" + traceback.format_exc()
    #         await self.bot.cogs['Exception Logging'].log_exception(error)
    #         await progress_msg.edit(embed=progress_embed.error())
    #
    # @commands.command('droptimizer_search')
    # async def search_droptimizer_data(self, ctx: commands.Context, team: str, difficulty: str, search_type: str,
    #                                   search_string: str, mobile_friendly: str = ""):
    #     """ Gives a list of the highest upgrades per item or boss. """
    #     # Check parameters for validity
    #     if team.lower() not in ['wb', 'cc']:
    #         await ctx.send('Invalid team. Please use `WB` or `CC`.')
    #         return
    #     if difficulty.lower() not in ['mythic', 'heroic', 'normal']:
    #         await ctx.channel.send('Invalid difficulty. Valid options: Mythic, Heroic, Normal')
    #         return
    #     if search_type.lower() not in ['boss', 'item']:
    #         await ctx.channel.send('Invalid type. Valid options: Boss, Item')
    #         return
    #
    #     # get embed and send it
    #     search_embed = DroptimizerService.search_droptimizer_data(difficulty.capitalize(),
    #                                                               team.lower(),
    #                                                               search_type.lower(),
    #                                                               search_string)
    #     if mobile_friendly.lower() == "mf":
    #         await ctx.send(embed=search_embed.get_mobile_friendly_embed())
    #     else:
    #         await ctx.send(embed=search_embed.get_embed())


async def setup(bot: commands.Bot):
    await bot.add_cog(DroptimizerCog(bot))