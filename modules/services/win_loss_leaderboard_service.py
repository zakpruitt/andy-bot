import json
import os

from modules.embeds.w_l_leaderboard_embed import WinLossLeaderboardEmbed


class WinLossLeaderboardService:

    @staticmethod
    def count_w_l_reaction(emoji, discord_name):
        with open(os.getenv("BOT_PATH") + 'resources/w_l_count.json', 'r+') as f:
            # get the current reactions dictionary
            current_w_l_count = {}
            try:
                current_w_l_count = json.load(f)
            except json.JSONDecodeError:
                pass

            # increment the "W" or "L" count for the user
            if discord_name in current_w_l_count:
                current_w_l_count[discord_name][str(emoji)] += 1
            else:
                current_w_l_count[discord_name] = {"🇼": 0, "🇱": 0}
                current_w_l_count[discord_name][str(emoji)] += 1

            # write the reactions dictionary to a JSON file
            f.seek(0)
            json.dump(current_w_l_count, f)
            f.truncate()

    @staticmethod
    def get_w_l_leaderboard():
        return WinLossLeaderboardEmbed("W/L Leaderboard")