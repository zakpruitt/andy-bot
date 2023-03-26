import os

import discord

from modules.embeds.abstract_embed import AbstractEmbed
from modules.utilities.general_utility import GeneralUtility
from modules.utilities.wow_utility import WowUtility


class AAApplicantEmbed(AbstractEmbed):

    def __init__(self, applicant):
        self.applicant = applicant
        self.color = WowUtility.get_class_color(applicant.wow_class)
        self.icon = WowUtility.get_class_icon(applicant.wow_class)

    def get_description(self):
        time, date = GeneralUtility.get_time_and_date()
        return f"This application was posted at {time} on {date}."

    def get_embed(self):
        embed = discord.Embed(title=f":bookmark_tabs: Application for {os.getenv('TEAM_NAME')}",
                              description=self.get_description(),
                              color=self.color)
        self.add_field_line_break(embed)

        # name/age/bnet
        embed.add_field(name="✍️ Name",
                        value=f"{self.applicant.character_name}",
                        inline=True)
        embed.add_field(name="🔞 Age",
                        value=f"{self.applicant.age}",
                        inline=True)
        embed.add_field(name="<:bnet:1070180625430089728> Battle.net",
                        value=f"{self.applicant.battlenet_contact}",
                        inline=True)
        self.add_field_line_break(embed)

        # discord/class/spec
        embed.add_field(name="<:discord:1070180627028131870> Discord",
                        value=f"{self.applicant.discord_contact}",
                        inline=True)
        embed.add_field(name=f"{self.icon} Class",
                        value=f"{self.applicant.wow_class}",
                        inline=True)
        embed.add_field(name="⚔️ Spec",
                        value=f"{self.applicant.primary_spec}",
                        inline=True)
        self.add_field_line_break(embed)

        # links
        embed.add_field(name="<:wcl:1070180727892758608> WCL",
                        value=f"[Click Here]({self.applicant.warcraftlogs_link})",
                        inline=True)
        embed.add_field(name="<:rio:1070180628131225732> R.IO",
                        value=f"[Click Here]({self.applicant.raiderio_link})",
                        inline=True)
        embed.add_field(name="<:wow:1070181155279745094> WCA",
                        value=f"[Click Here]({self.applicant.armory_link})",
                        inline=True)
        self.add_field_line_break(embed)

        # real life
        embed.add_field(name="📖 Tell us about yourself in real life!",
                        value=f"{self.applicant.real_life_summary}",
                        inline=False)
        self.add_field_line_break(embed)

        # skills summary
        embed.add_field(name="🎯 What experience, skill, and attitude will you bring to the guild?",
                        value=f"{self.applicant.skills_summary}",
                        inline=False)
        self.add_field_line_break(embed)

        # proclivity
        embed.add_field(name="🎮 How often do you play WoW?",
                        value=f"{self.applicant.proclivity_summary}",
                        inline=False)

        self.add_field_line_break(embed)

        # pizza question
        embed.add_field(name="🍕 Does pineapple belong on pizza?",
                        value=f"{self.applicant.pizza_question}",
                        inline=False)

        # footer
        embed.set_footer(text="Mist Recruiting",
                         icon_url="https://raw.githubusercontent.com/mist-guild/mist-rustbolt/master/public/logo192.png")
        self.add_field_line_break(embed)

        return embed

    def error(self):
        self.color = 0xff0000
        embed = self.get_embed()
        embed.description += f'\n\nError during applicant embed posting! Check logs.'
        return embed
