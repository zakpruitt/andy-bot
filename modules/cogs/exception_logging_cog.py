import os

from discord.ext import commands

from modules.utilities.general_utility import GeneralUtility


class ExceptionLoggingCog(commands.Cog, name="Exception Logging"):
    """ Tyrhold's custom error logging cog. """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def log_exception(self, error):
        log_channel = self.bot.get_channel(int(os.environ.get("ERROR_LOG_ID")))
        if log_channel:
            time, date = GeneralUtility.get_time_and_date()
            message = f"Error occurred at {time} on {date}!\n\n```{error}```\n"
            await log_channel.send(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(ExceptionLoggingCog(bot))