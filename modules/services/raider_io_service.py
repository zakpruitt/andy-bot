from apis.raider_io_api import RaiderIoApi
from modules.embeds.raider_io_history_embed import RaiderIoHistoryEmbed


class RaiderIoService:

    @staticmethod
    def get_raider_io_history(name, realm, region):
        # get raider profile and format season data
        raider_profile = RaiderIoApi.get_profile_all_io_history(name, realm, region)
        mythic_plus_scores_by_season = {}
        for season_data in raider_profile.mythic_plus_scores_by_season:
            season_name = season_data['season']
            all_score = season_data['scores']['all']
            mythic_plus_scores_by_season[season_name] = all_score
        mythic_plus_scores_by_season = {k: v for k, v in mythic_plus_scores_by_season.items() if v != 0}

        # build and return embed
        return RaiderIoHistoryEmbed(raider_profile.name,
                                    raider_profile.class_name,
                                    raider_profile.thumbnail_url,
                                    raider_profile.profile_url,
                                    mythic_plus_scores_by_season,
                                    raider_profile.last_crawled_at)
