import os
import re
import traceback
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands

from modules.services.recruit_service import RecruitService


class RecruitCog(commands.Cog, name="Recruit"):
    """Mist Bot's interaction with the Recruit Webhook"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.RECRUIT_WEBHOOK_ID = int(os.getenv("RECRUIT_WEBHOOK_ID"))
        self.RECRUIT_CATEGORY_ID = int(os.getenv("RECRUIT_CATEGORY_ID"))

    @cog_ext.cog_slash(
        name="ping",
        description="Ping the bot",
        guild_ids=[1078792618651168850],
    )
    async def ping(self, ctx: SlashContext):
        await ctx.send("Pong!")


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitCog(bot))
