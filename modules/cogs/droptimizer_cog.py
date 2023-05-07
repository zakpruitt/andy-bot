import os
import traceback

from discord.ext import commands

from modules.services.droptimizer_service import DroptimizerService
from modules.utilities.google_sheets_utility import GoogleSheetsUtility


class DroptimizerCog(commands.Cog, name="Droptimizer"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.DROPTIMIZER_CHANNEL_ID = int(os.getenv("DEV_DROPTIMIZER_CHANNEL_ID"))
        self.sheets_util = GoogleSheetsUtility(os.getenv('DROPTIMIZER_SPREADSHEET_NAME'))

    @commands.command(name="droprun")
    async def run_droptimizer_reports(self, ctx: commands.Context):
        """ Parses all input Droptimizer Links. """
        try:
            # make this into a specific embed
            progress_embed = DroptimizerService.get_progress_embed()
            progress_msg = await ctx.send(embed=progress_embed.get_embed())
            await DroptimizerService.process_droptimizer_reports(progress_embed, progress_msg)
        except Exception as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
            await progress_msg.edit(embed=progress_embed.error())

    @commands.command('dropsearch')
    async def search_droptimizer_data(self, ctx: commands.Context, difficulty: str, search_type: str,
                                      search_string: str, mobile_friendly: str = ""):
        """ Gives a list of the highest upgrades per item or boss. """
        # Check parameters for validity
        if difficulty.lower() not in ['mythic', 'heroic', 'normal']:
            await ctx.channel.send('Invalid difficulty. Valid options: Mythic, Heroic, and Normal')
            return
        if search_type.lower() not in ['boss', 'item']:
            await ctx.channel.send('Invalid type. Valid options: Boss, Item')
            return

        # get embed and send it
        search_embed = DroptimizerService.search_droptimizer_data(difficulty.capitalize(),
                                                                  search_type.lower(),
                                                                  search_string)
        if mobile_friendly.lower() == "mf":
            await ctx.send(embed=search_embed.get_mobile_friendly_embed())
            return
        await ctx.send(embed=search_embed.get_embed())

    @commands.Cog.listener()
    async def on_message(self, message):
        """ Listens for Droptimizer links and appends them to the spreadsheet. """
        if message.channel.id != self.DROPTIMIZER_CHANNEL_ID:
            return

        mention = message.author.mention
        try:
            if 'https://www.raidbots.com/simbot/report' in message.content:
                links_processed = await DroptimizerService.add_droptimizer_report(message.content)
                await message.delete()
                await message.channel.send(f"I successfully processed {links_processed} link(s). Thank you, {mention}! <:tier5:1085390493778710683>")
        except Exception as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
            await message.channel.send(f"There was an error processing your droptimizer report(s), {mention}. "
                                       f"<:TrollDespair:1081251201951223819>\n\nPlease verify your link(s) are correct"
                                       f"! If your link(s) are valid and issues persist, please ping an "         
                                       f"officer. <:Okayge:1103488695174189177> 👍")


async def setup(bot: commands.Bot):
    await bot.add_cog(DroptimizerCog(bot))
