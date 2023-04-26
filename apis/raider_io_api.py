from raiderio import RaiderIO

from apis.dataclasses.raider_io_profile import RaiderIoProfile


class RaiderIoApi:
    api_client = RaiderIO()
    MYTHIC_PLUS_SEASONS = ["season-df-2", "season-df-1", "season-sl-4", "season-sl-3", "season-sl-2", "season-sl-1",
                           "season-bfa-4", "season-bfa-3", "season-bfa-2", "season-bfa-1", "season-7.3.0",
                           "season-7.2.0"]

    @classmethod
    def get_profile_all_io_history(cls, name, realm, region):
        # get all seasons response
        mythic_plus_scores_by_season = "mythic_plus_scores_by_season:" + ":".join(cls.MYTHIC_PLUS_SEASONS)
        response = cls.api_client.get_character_profile(region, realm, name, mythic_plus_scores_by_season)

        # change class to class_name and build profile
        response['class_name'] = response['class']
        response.pop('class')
        return RaiderIoProfile(**response)