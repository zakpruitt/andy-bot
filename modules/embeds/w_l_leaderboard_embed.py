import discord
from table2ascii import table2ascii as t2a, PresetStyle, Alignment

from modules.embeds.abstract_embed import AbstractEmbed
from modules.utilities.general_utility import GeneralUtility


class WinLossLeaderboardEmbed(AbstractEmbed):

    def __init__(self, title, current_w_l_count):
        self.title = title
        self.color = 0x27c6f2
        self.current_w_l_count = current_w_l_count

    def get_description(self):
        description = []
        headers = ["Name", "W", "L"]
        for discord_name, w_l_count in self.current_w_l_count.items():
            description.append([discord_name, w_l_count["🇼"], w_l_count["🇱"]])
        return t2a(
            header=headers,
            body=description,
            style=PresetStyle.ascii_borderless,
            alignments=[Alignment.LEFT, Alignment.CENTER, Alignment.CENTER]
        )

    def get_embed(self):
        embed = discord.Embed(title=self.title, description=f"```{self.get_description()}```", color=self.color)
        time, date = GeneralUtility.get_time_and_date()
        embed.set_author(name=f"Generated at {time} on {date}",
                         icon_url="https://raw.githubusercontent.com/zakpruitt/andy-bot/master/resources/images/andy_logo_simple.png")
        embed.set_thumbnail(
            url="https://static-00.iconduck.com/assets.00/regional-indicator-symbol-letter-w-emoji-1024x1024-7gg9i57v.png")
        return embed

    def get_mobile_friendly_embed(self):
        embed = discord.Embed(title=self.title, description=self.get_mobile_friendly_description(), color=self.color)
        time, date = GeneralUtility.get_time_and_date()
        embed.set_author(name=f"Generated at {time} on {date}",
                         icon_url="https://raw.githubusercontent.com/zakpruitt/andy-bot/master/resources/images/andy_logo_simple.png")
        embed.set_thumbnail(
            url="https://static-00.iconduck.com/assets.00/regional-indicator-symbol-letter-w-emoji-1024x1024-7gg9i57v.png")
        return embed

    def error(self):
        self.color = 0xff0000
        embed = self.get_embed()
        embed.description += f'\n\nError during search! Check logs.'
        return embed
