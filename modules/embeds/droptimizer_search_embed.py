import discord
from table2ascii import table2ascii as t2a, PresetStyle, Alignment

from modules.embeds.abstract_embed import AbstractEmbed
from modules.utilities.general_utility import GeneralUtility


class DroptimizerSearchEmbed(AbstractEmbed):

    def __init__(self, title, icon_url, dataframe, search_type):
        self.title = title
        self.icon_url = icon_url
        self.dataframe = dataframe
        self.search_type = search_type
        self.color = 0x27c6f2

    def get_description(self):
        description = []
        if self.search_type.lower() == "boss":
            headers = ["Name", "DPS Gain", "Item Name"]
            for character_name, row in self.dataframe.iterrows():
                item_name = row["Item"]
                character_abbrv = GeneralUtility.get_spec_abbreviation(character_name)
                description.append([character_abbrv, "{:.1f}".format(row["Max Value"]), item_name[0:15]])
            return t2a(
                header=headers,
                body=description,
                style=PresetStyle.ascii_borderless,
                alignments=[Alignment.LEFT, Alignment.DECIMAL, Alignment.CENTER]
            )
        elif self.search_type.lower() == "item":
            headers = ["Name", "DPS Gain"]
            for character_name, row in self.dataframe.iterrows():
                character_abbrv = GeneralUtility.get_spec_abbreviation(character_name)
                description.append([character_abbrv, "{:.1f}".format(row["Max Value"])])
            return t2a(
                header=headers,
                body=description,
                style=PresetStyle.ascii_borderless,
                alignments=[Alignment.LEFT, Alignment.DECIMAL]
            )

    def get_mobile_friendly_description(self):
        description = []
        for index, row in self.dataframe.iterrows():
            item_name = row["Item"]
            description.append(f"> {item_name}\n> {index} - {row['Max Value']:.2f}")
        return '\n\n'.join(description)

    def get_embed(self):
        embed = discord.Embed(title=self.title, description=f"```{self.get_description()}```", color=self.color)
        time, date = GeneralUtility.get_time_and_date()
        embed.set_author(name=f"Generated at {time} on {date}",
                         icon_url="https://raw.githubusercontent.com/zakpruitt/andy-bot/master/resources/images/andy_logo_simple.png")
        embed.set_thumbnail(url=self.icon_url)
        return embed

    def get_mobile_friendly_embed(self):
        embed = discord.Embed(title=self.title, description=self.get_mobile_friendly_description(), color=self.color)
        time, date = GeneralUtility.get_time_and_date()
        embed.set_author(name=f"Generated at {time} on {date}",
                         icon_url="https://raw.githubusercontent.com/zakpruitt/andy-bot/master/resources/images/andy_logo_simple.png")
        embed.set_thumbnail(url=self.icon_url)
        return embed

    def error(self):
        self.color = 0xff0000
        embed = self.get_embed()
        embed.description += f'\n\nError during search! Check logs.'
        return embed
