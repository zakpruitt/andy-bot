import traceback

from discord.ext import commands

from modules.services.raider_io_service import RaiderIoService


class RaiderIoCog(commands.Cog, name="Raider IO"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command('riohistory')
    async def get_io_history(self, ctx: commands.Context, name: str, realm: str, region: str = 'us'):
        """ Displays a player's raider.io history. """
        try:
            msg = await ctx.send(f"Retrieving {name}'s Raider.IO history...")
            embed = RaiderIoService.get_raider_io_history(name, realm, region)
            await msg.edit(content="", embed=embed)
        except Exception as error:
            await self.bot.cogs['Exception Logging'].log_exception(error, traceback.format_exc())
            await msg.edit(embed=embed.error())


async def setup(bot: commands.Bot):
    await bot.add_cog(RaiderIoCog(bot))
