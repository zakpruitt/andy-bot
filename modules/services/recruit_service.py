import discord

from modules.utilities.discord_utility import DiscordUtility
from modules.utilities.general_utility import GeneralUtility


class RecruitService:

    @staticmethod
    async def close_application(interaction):
        await interaction.channel.edit(name=f"[Closed] {interaction.channel.name}", archived=True, locked=True)
        time, date = GeneralUtility.get_time_and_date()
        await interaction.response.send_message(
            f'Thread {interaction.channel.mention} was closed and locked on {date} at {time}.')

    @classmethod
    async def generate_trial_channel(cls, interaction, recruit_name=None, discord_name=None):
        # get required variables
        category = DiscordUtility.get_category_by_id(interaction.guild, 1089899690717360218)
        recruit_trial_role = DiscordUtility.get_role_by_id(interaction.guild, 1079193586056302602)
        recruiter_role = DiscordUtility.get_role_by_id(interaction.guild, 1080222880719175781)
        officer_role = DiscordUtility.get_role_by_id(interaction.guild, 1078793314188398592)
        bot_role = DiscordUtility.get_role_by_id(interaction.guild, 1089668616384938070)

        # Get the recruit's Discord name
        if discord_name is None and recruit_name is None:
            recruit_embed = await cls.__get_recruit_embed(interaction.channel)
            recruit_name = recruit_embed.fields[0].value.split(" - ")[0]
            discord_name = recruit_embed.fields[4].value
        recruit_member = DiscordUtility.get_member_by_discord_name(interaction.guild, discord_name)
        if not recruit_member:
            await interaction.response.send_message(
                f"Could not find a member with the name {discord_name}. Please invite them before invoking this command.")
            return

        # Create a new channel under the category
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            recruiter_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            bot_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            officer_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            recruit_member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        channel_name = f"trial-{recruit_name}"
        new_channel = await interaction.guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

        # Populate the trial channel and permit roles
        await new_channel.send(f"Hey, {recruit_member.mention}!! 👋 Welcome to your own, personal trial channel. "
                               f"<:BatChest:1082112942541123716>\n\nThis channel is meant to be a private and direct "
                               f"line of communication between yourself and the officers. This may include log "
                               f"reviews, log analysis, conversation about strategies, etc. Expect feedback at least "
                               f"once a week, typically between Thursday - Monday. "
                               f"<:BASED:1079179696765411414>\n\nFeel free to ping ANY officer. We are here to help "
                               f"you succeed! Specifically, ping <@305491314286526474> for performance or healing "
                               f"related needs/questions, <@124689347818684419> for any strategy/composition related "
                               f"needs/questions, and <@64833312220250112> for anything else! <a:pepeJAM:1081251169906724864>"
                               f"\n\nWe "
                               f"provide six versatility phials, pot cauldrons, feasts, repairs (during raid), "
                               f"and vantus runes. It is expected you bring any other ancillary consumables ("
                               f"inscription runes, etc.) and are FULLY enchanted (this includes tertiaries). "
                               f"Required addons outside of the typical ones are MRT (Method Raid Tools) and RC Loot "
                               f"Council. As a reminder, we raid M, T, TH 10 PM - 1 AM CST. It is expected raiders "
                               f"are present at least by 9:50 PM. <a:LETSGOOO:1081251215796604979>\n\nTrials can "
                               f"participate in boosts starting from day 1, so feel free to sign up in "
                               f"<#1092128300563964046>! Other than that, please keep an eye on "
                               f"<#1079191097743519835> for roster postings and have fun!! "
                               f"<:GAmer:1081034983558348800> <a:HYPERCLAP:1081251217147187252>")
        await recruit_member.add_roles(recruit_trial_role)
        await interaction.send(f"Created a new channel {new_channel.mention} under the category {category.name}.")
        await interaction.send(f"Given the role {recruit_trial_role.mention} to {recruit_member.mention}.")

    @staticmethod
    async def __get_recruit_embed(channel):
        async for message in channel.history(oldest_first=True):
            if message.embeds:
                return message.embeds[0]
        return None
