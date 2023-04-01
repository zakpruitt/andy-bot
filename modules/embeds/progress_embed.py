from collections import OrderedDict

import discord

from modules.embeds.abstract_embed import AbstractEmbed
from modules.utilities.general_utility import GeneralUtility

UNICODE_CHECKMARK = '\u2705'
UNICODE_CROSSMARK = '\u274C'


class ProgressEmbed(AbstractEmbed):

    def __init__(self, title, steps_list):
        self.title = title
        self.color = 0x27c6f2
        self.steps = OrderedDict()
        for step in steps_list:
            self.steps[step] = False

    def get_description(self):
        desc = 'A new droptimizer report has been submitted! Please wait until the report has been processed. This is indicated by all green checkmarks below.\n\n You can view the AotC Andy droptimizer sheet [here](https://docs.google.com/spreadsheets/d/1LFUr61R9AewV3RDbIsz3Ibiivqm6IrISPl7QrZcF6XQ/edit#gid=1346039081).\n\n'
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
        # TODO: As we have more progress ones, we need to make this a parent class, then a droptimizer progress child embed.
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
