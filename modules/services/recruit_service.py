import discord

from modules.utilities.discord_utility import DiscordUtility
from modules.utilities.general_utility import GeneralUtility


class RecruitService:

    @staticmethod
    async def close_application(ctx):
        await ctx.channel.edit(name=f"[Closed] {ctx.channel.name}", archived=True, locked=True)
        time, date = GeneralUtility.get_time_and_date()
        await ctx.send(
            f'Thread {ctx.channel.mention} was closed and locked by {ctx.author.mention} on {date} at {time}.')

    @classmethod
    async def generate_trial_channel(cls, ctx):
        # get required variables
        category = DiscordUtility.get_category_by_id(ctx.guild, 1089899690717360218)
        tech_support_role = DiscordUtility.get_role_by_id(ctx.guild, 1089766156505727047)
        officer_role = DiscordUtility.get_role_by_id(ctx.guild, 1078793314188398592)

        # Get the recruit's Discord name
        recruit_embed = await cls.__get_recruit_embed(ctx.channel)
        recruit_name = recruit_embed.fields[0].value
        discord_name = recruit_embed.fields[4].value
        recruit_member = DiscordUtility.get_member_by_discord_name(ctx.guild, discord_name)
        if not recruit_member:
            await ctx.send(
                f"Could not find a member with the name {discord_name}. Please invite them before invoking this command.")
            return

        # Create a new channel under the category
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            tech_support_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            officer_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            recruit_member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel_name = f"trial-{recruit_name}"
        new_channel = await ctx.guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

        # Populate the trial channel
        await new_channel.send(f"Hey, {recruit_member.mention}!! 👋 Welcome to your own, personal trial channel. "
                               f"<:BatChest:1082112942541123716>\n\nThis channel is meant to be a private and direct "
                               f"line of communication between yourself and the officers. This may include log "
                               f"reviews, log analysis, conversation about strategies, etc. Expect feedback at least "
                               f"once a week, typically between Thursday - Monday. "
                               f"<:BASED:1079179696765411414>\n\nFeel free to ping ANY officer. We are here to help "
                               f"you succeed! Specifically, ping <@305491314286526474> for performance related "
                               f"needs/questions, <@124689347818684419> for any strategy/composition related "
                               f"needs/questions, <@620849124912398337> for healing related needs/questions, "
                               f"and <@64833312220250112> for anything else! <a:pepeJAM:1081251169906724864>\n\nWe "
                               f"provide six versatility phials, pot cauldrons, feasts, repairs (during raid), "
                               f"and vantus runes. It is expected you bring any other ancillary consumables ("
                               f"inscription runes, etc.) and are FULLY enchanted (this includes tertiaries). "
                               f"Required addons outside of the typical ones are MRT (Method Raid Tools) and RC Loot "
                               f"Council. As a reminder, we raid M, T, TH 10 PM - 1 AM CST. It is expected raiders "
                               f"are present at least by 9:50 PM. <a:LETSGOOO:1081251215796604979>\n\nTrials can "
                               f"participate in boosts starting from day 1, so feel free to sign up in "
                               f"<#1079194103193026640>! Other than that, please keep an eye on "
                               f"<#1079191097743519835> for roster postings and have fun!! "
                               f"<:GAmer:1081034983558348800> <a:HYPERCLAP:1081251217147187252>")
        await ctx.send(f"Created a new channel {new_channel.mention} under the category {category.name}.")
        await cls.close_application(ctx)

    @staticmethod
    async def __get_recruit_embed(channel):
        async for message in channel.history(oldest_first=True):
            if message.embeds:
                return message.embeds[0]
        return None
