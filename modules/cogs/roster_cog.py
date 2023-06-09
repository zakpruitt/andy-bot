from discord.ext import commands

from modules.services.roster_service import RosterService


class RosterCog(commands.Cog, name="Roster"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("ass")
    async def based(self, ctx: commands.Context):
        """ based. """
        RosterService.a()


async def setup(bot: commands.Bot):
    await bot.add_cog(RosterCog(bot))
