import os

from discord.ext import commands

from modules.services.recruit_service import RecruitService


class RecruitCog(commands.Cog, name="Recruit"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.RECRUIT_FORUM_ID = int(os.getenv("PROD_RECRUIT_FORUM_ID"))

    @commands.command("close")
    async def close_application(self, ctx: commands.Context):
        if ctx.channel.parent_id != self.RECRUIT_FORUM_ID:
            return
        await RecruitService.close_application(ctx)

    @commands.command("trial")
    async def trial_applicant(self, ctx: commands.Context):
        if ctx.channel.parent_id != self.RECRUIT_FORUM_ID:
            return
        await RecruitService.generate_trial_channel(ctx)


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitCog(bot))