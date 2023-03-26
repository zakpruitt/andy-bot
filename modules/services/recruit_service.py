import asyncio
import base64
import os
import zlib

from apis.dataclasses.applicant import Applicant
from apis.mist import Mist
from modules.embeds.mist_applicant_embed import MistApplicantEmbed
from modules.utilities.discord_utility import DiscordUtility


class RecruitService:
    RECRUIT_CATEGORY_ID = int(os.getenv("RECRUIT_CATEGORY_ID"))
    RECRUIT_FORUM_ID = int(os.getenv("RECRUIT_FORUM_ID"))
    BOT_ID = int(os.getenv("BOT_ID"))

    @classmethod
    async def generate_recruit_text_channel(cls, message):
        # get embed and guild
        embed = message.embeds[0]
        guild = message.guild

        # get name, id, and team name
        author_split = embed.author.name.split("•")
        recruit_name = author_split[0].strip().split("-")[0]
        recruit_id = author_split[1].strip()

        # create text channel
        channel_name = f"{recruit_name}-{recruit_id}"
        recruit_forum = DiscordUtility.get_channel_by_id(guild, cls.RECRUIT_FORUM_ID)
        title = 'Bigchomper * 1'

        applicant = Applicant.build_from_id(1)
        app_embed = MistApplicantEmbed(applicant)

        # Create a new thread for the post
        post = await recruit_forum.create_thread(name=title, embed=app_embed.get_embed())

        # update embed
        embed.url = post.thread.jump_url
        await message.delete()
