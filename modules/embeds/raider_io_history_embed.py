import json
import os

import discord

from modules.embeds.abstract_embed import AbstractEmbed
from modules.utilities.general_utility import GeneralUtility


class RaiderIoHistoryEmbed(AbstractEmbed):
    SEASON_NAME_ICON_MAP = {
        "season-df-2": ":question: DF Season 2",
        "season-df-1": "<:Raszageth:1100630578958696450> DF Season 1",
        "season-sl-4": "<:Fated:1100631692458340422> SL Season 4",
        "season-sl-3": "<:Jailer:1100630580783235142> SL Season 3",
        "season-sl-2": "<:Sylvanus:1100630578014978059> SL Season 2",
        "season-sl-1": "<:Denathrius:1100628791740616704> SL Season 1",
        "season-bfa-4": "<:Nzoth:1100630577117409280> BFA Season 4",
        "season-bfa-3": "<:Azshara:1100630566690373733> BFA Season 3",
        "season-bfa-2": "<:Jaina:1100630569169190922> BFA Season 2",
        "season-bfa-1": "<:Ghuun:1100630575364186143> BFA Season 1",
        "season-7.3.0": "<:Argus:1100630565633400944> Legion Season 3",
        "season-7.2.0": "<:Kiljaden:1100630568271626330>  Legion Season 2",
    }

    def __init__(self, name, class_name, thumbnail_url, profile_url, mythic_plus_scores_by_season, last_crawled_at):
        self.title = f"Raider IO History for {name}"
        self.class_name = class_name
        self.class_icon, self.color = self._get_class_info()
        self.thumbnail_url = thumbnail_url
        self.profile_url = profile_url
        self.mythic_plus_scores_by_season = mythic_plus_scores_by_season
        self.last_crawled_at = last_crawled_at

    def _get_class_info(self):
        with open(os.getenv("BOT_PATH") + 'resources/class_icon_map.json', 'r') as icon_map, \
                open(os.getenv("BOT_PATH") + 'resources/class_color_map.json', 'r') as color_map:
            color_value = json.load(color_map)[self.class_name]
            return json.load(icon_map)[self.class_name], discord.Colour(int(color_value, 16))

    def get_description(self):
        return "\n"

    def get_embed(self):
        # build embed
        embed = discord.Embed(title=self.title,
                              description=self.get_description(),
                              color=self.color,
                              url=self.profile_url)
        embed.set_thumbnail(url=self.thumbnail_url)
        embed.set_footer(text=f"Last crawled at {self.last_crawled_at[0:19]}")

        # add fields for each season
        for idx, (season, score) in enumerate(self.mythic_plus_scores_by_season.items()):
            if idx % 3 == 0 and idx != 0:
                self.add_field_line_break(embed)
            if idx == len(self.mythic_plus_scores_by_season) - 1 and len(self.mythic_plus_scores_by_season) % 3 != 0:
                embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name=self.SEASON_NAME_ICON_MAP[season], value=score, inline=True)


        # add AA author and timestamp
        time, date = GeneralUtility.get_time_and_date()
        embed.set_author(name=f"Generated at {time} on {date}",
                         icon_url="https://raw.githubusercontent.com/zakpruitt/andy-bot/master/resources/images/andy_logo_simple.png")
        return embed

    def error(self):
        self.color = 0xff0000
        embed = self.get_embed()
        embed.description += f'\n\nError during IO history look up! Check logs.'
        return embed
