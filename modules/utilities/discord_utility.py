import discord


class DiscordUtility:

    @staticmethod
    def get_category_by_id(guild, category_id):
        return discord.utils.get(guild.categories, id=category_id)

    @staticmethod
    def get_channel_by_id(guild, channel_id):
        return discord.utils.get(guild.channels, id=channel_id)

    @staticmethod
    def get_role_by_id(guild, role_id):
        return discord.utils.get(guild.roles, id=role_id)

    @staticmethod
    def get_member_by_discord_name(guild, member_name):
        if "#" in member_name:
            return discord.utils.get(guild.members,
                                     name=member_name.split("#")[0],
                                     discriminator=member_name.split("#")[1])
        else:
            return discord.utils.get(guild.members,
                                     name=member_name)
