import os

import discord
from discord import app_commands
from discord.ext import commands

from modules.services.recruit_service import RecruitService


class RecruitCog(commands.Cog, name="Recruit"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.RECRUIT_FORUM_ID = int(os.getenv("PROD_RECRUIT_FORUM_ID"))

    @app_commands.command(name="close_application", description="Closes, locks, and sends a notifying message in a "
                                                                "recruit application.")
    async def close_application(self, interaction: discord.Interaction):
        if interaction.channel.parent_id != self.RECRUIT_FORUM_ID:
            return
        await RecruitService.close_application(interaction)

    @app_commands.command(name="trial_applicant", description="Spawns a trial channel and adds all required members "
                                                              "to the channel.")
    async def trial_applicant(self, interaction: discord.Interaction, recruit_name: str = None,
                              discord_name: str = None):
        if interaction.channel.parent_id != self.RECRUIT_FORUM_ID:
            return
        trial_channel = await RecruitService.generate_trial_channel(interaction, recruit_name, discord_name)
        await interaction.response.send_message(f"Created a new channel {trial_channel.mention}.")

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id != self.RECRUIT_FORUM_ID:
            return

        # get context from initial message population
        async for message in thread.history(limit=1):
            first_message = message
        ctx = await self.bot.get_context(first_message)
        fields = thread.name.split(" - ")
        await self.bot.cogs['Raider IO'].get_io_history(ctx, fields[0], fields[1])


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitCog(bot))
