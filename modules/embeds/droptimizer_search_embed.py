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
        # get description as list of lists
        description = []
        headers = ["Name", "DPS Gain", "Item Name"]
        for index, row in self.dataframe.iterrows():
            item_name = row["Item"].split(' - ')[1].strip()
            description.append([index, "{:.1f}".format(row["Max Value"]), item_name[0:15]])

        # return ascii table
        return t2a(
            header=headers,
            body=description,
            style=PresetStyle.ascii_borderless,
            alignments=[Alignment.LEFT, Alignment.DECIMAL, Alignment.CENTER]
        )

    def get_mobile_friendly_description(self):
        description = []
        for index, row in self.dataframe.iterrows():
            item_name = row["Item"].split(' - ')[1].strip()
            description.append(f"> {item_name}\n> {index} - {row['Max Value']:.2f}")
        return '\n\n'.join(description)

    def get_embed(self):
        embed = discord.Embed(title=self.title, description=f"```{self.get_description()}```", color=self.color)
        time, date = GeneralUtility.get_time_and_date()
        embed.set_author(name=f"Generated at {time} on {date}",
                         icon_url="https://raw.githubusercontent.com/mist-guild/mist-rustbolt/master/public/logo192.png")
        embed.set_thumbnail(url=self.icon_url)
        return embed

    def get_mobile_friendly_embed(self):
        embed = discord.Embed(title=self.title, description=self.get_mobile_friendly_description(), color=self.color)
        time, date = GeneralUtility.get_time_and_date()
        embed.set_author(name=f"Generated at {time} on {date}",
                         icon_url="https://raw.githubusercontent.com/mist-guild/mist-rustbolt/master/public/logo192.png")
        embed.set_thumbnail(url=self.icon_url)
        return embed

    def error(self):
        self.color = 0xff0000
        embed = self.get_embed()
        embed.description += f'\n\nError during search! Check logs.'
        return embed
