from dataclasses import dataclass

from apis.dataclasses.mythic_plus_score import MythicPlusScore


@dataclass
class MythicPlusSeason:
    season: str
    scores: dict[str, float]
    segments: dict[str, MythicPlusScore]
