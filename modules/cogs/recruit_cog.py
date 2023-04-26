import os

from discord.ext import commands

from modules.services.recruit_service import RecruitService


class RecruitCog(commands.Cog, name="Recruit"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.RECRUIT_FORUM_ID = int(os.getenv("PROD_RECRUIT_FORUM_ID"))

    @commands.command("close")
    async def close_application(self, ctx: commands.Context):
        """ Closes, locks, and sends a notifying message in a recruit application. """
        if ctx.channel.parent_id != self.RECRUIT_FORUM_ID:
            return
        await RecruitService.close_application(ctx)

    @commands.command("trial")
    async def trial_applicant(self, ctx: commands.Context, recruit_name=None, discord_name=None):
        """ Spawns a trial channel and adds all required members to the channel. """
        if ctx.channel.parent_id != self.RECRUIT_FORUM_ID:
            return
        await RecruitService.generate_trial_channel(ctx, recruit_name, discord_name)

    @commands.Cog.listener()
    async def on_thread_create(self, thread):

        await thread.send("hello")


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitCog(bot))
