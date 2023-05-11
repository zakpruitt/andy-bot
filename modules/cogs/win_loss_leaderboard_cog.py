import discord
from discord import app_commands
from discord.ext import commands

from modules.services.win_loss_leaderboard_service import WinLossLeaderboardService


class WinLossLeaderboardCog(commands.Cog, name="WL Leaderboard"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="show_w_l_leaderboard", description="Displays the W/L leaderboard in an embed.")
    async def show_w_l_leaderboard(self, interaction: discord.Interaction):
        embed = WinLossLeaderboardService.get_w_l_leaderboard()
        await interaction.response.send_message(embed=embed.get_embed())

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji
        if str(emoji) in ["🇼", "🇱"]:
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            discord_message_author = str(message.author)
            discord_reactor = str(payload.member)
            if discord_message_author != discord_reactor:
                WinLossLeaderboardService.count_w_l_reaction(emoji, discord_message_author)


async def setup(bot: commands.Bot):
    await bot.add_cog(WinLossLeaderboardCog(bot))
