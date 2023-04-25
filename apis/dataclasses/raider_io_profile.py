from dataclasses import dataclass
from typing import List

from apis.dataclasses.mythic_plus_season import MythicPlusSeason


@dataclass
class RaiderIoProfile:
    name: str
    race: str
    class_name: str
    active_spec_name: str
    active_spec_role: str
    gender: str
    faction: str
    achievement_points: int
    honorable_kills: int
    thumbnail_url: str
    region: str
    realm: str
    last_crawled_at: str
    profile_url: str
    profile_banner: str
    mythic_plus_scores_by_season: List[MythicPlusSeason]