from collections import OrderedDict

import discord

from modules.embeds.abstract_embed import AbstractEmbed
from modules.utilities.general_utility import GeneralUtility

UNICODE_CHECKMARK = '\u2705'
UNICODE_CROSSMARK = '\u274C'


class ProgressEmbed(AbstractEmbed):

    def __init__(self, title, description, steps_list):
        self.title = title
        self.description = description
        self.color = 0x27c6f2
        self.steps = OrderedDict()
        for step in steps_list:
            self.steps[step] = False

    def get_description(self):
        desc = self.description + "\n\n"
        for step, status in self.steps.items():
            desc += '{0} {1}\n\n'.format(UNICODE_CHECKMARK if status else UNICODE_CROSSMARK, step)
        return desc

    def get_current_step(self):
        for step, status in self.steps.items():
            if not status:
                return step

    def advance_step(self):
        for step, status in self.steps.items():
            if not status:
                self.steps[step] = True
                break

    def get_embed(self):
        embed = discord.Embed(title=self.title, description=self.get_description(), color=self.color)
        time, date = GeneralUtility.get_time_and_date()
        embed.set_author(name=f"Generated at {time} on {date}")
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/943219769850785792/pohESfYc_400x400.jpg")
        return embed

    def error(self):
        self.color = 0xff0000
        embed = self.get_embed()
        embed.description += f'\n\nError at {self.get_current_step()}!'
        return embed
