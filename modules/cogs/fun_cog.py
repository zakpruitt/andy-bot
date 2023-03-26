from discord.ext import commands


class FunCog(commands.Cog, name="Fun"):
    """Fun commands! """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("wthis", hidden=True)
    async def react_w(self, ctx: commands.Context):
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        await message.add_reaction("w")


async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
