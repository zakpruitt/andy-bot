import discord


class DiscordUtility:
    @staticmethod
    def get_applicant_id_from_recruit_channel_name(channel_name):
        channel_split = channel_name.split("-")
        return channel_split[len(channel_split) - 1]

    @staticmethod
    def get_applicant_id_from_archive_channel_name(channel_name):
        channel_split = channel_name.split("-")
        return channel_split[len(channel_split) - 2]

    @staticmethod
    def get_category_by_id(guild, category_id):
        return discord.utils.get(guild.categories, id=category_id)

    @staticmethod
    def get_channel_by_id(guild, channel_id):
        return discord.utils.get(guild.channels, id=channel_id)

    @staticmethod
    async def create_text_channel(guild, channel_name, category):
        channel = await guild.create_text_channel(name=channel_name, category=category)
        return channel
