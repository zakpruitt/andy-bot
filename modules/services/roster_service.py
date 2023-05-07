import os

import numpy as np

from apis.raider_io_api import RaiderIoApi
from modules.utilities.google_sheets_utility import GoogleSheetsUtility


class RosterService:
    sheet = GoogleSheetsUtility(os.getenv('DROPTIMIZER_SPREADSHEET_NAME'))

    @staticmethod
    def total_item_upgrades_for_raider(raider, boss, droptimizer_data_difficulty_df):
        upgrades = droptimizer_data_difficulty_df.loc[boss, raider]
        positive_upgrades = np.where(upgrades > 0, upgrades, 0)
        return positive_upgrades.sum()

    @classmethod
    def a(cls):
        prog = RaiderIoApi.get_guild_current_raid_progression()

        # get roster priority
        roster_priority_sheet = cls.sheet.get_worksheet('Roster Priority')
        roster_priority_df = cls.sheet.get_as_df(roster_priority_sheet)

        # get droptimizer data
        worksheet = cls.sheet.get_data_worksheet()
        droptimizer_data_df = GoogleSheetsUtility.get_as_df(worksheet)
        droptimizer_data_difficulty_df = droptimizer_data_df.loc[droptimizer_data_df['Difficulty'] == "Mythic"]
        droptimizer_data_difficulty_df.dropna(how='all', axis='columns', inplace=True)
        droptimizer_data_difficulty_df.set_index(['Boss', 'Item'], inplace=True)
        droptimizer_data_difficulty_df.drop('Difficulty', axis=1, inplace=True)

        # Filter the roster priority DataFrame to include only DPS role raiders
        dps_raiders = roster_priority_df[roster_priority_df['Role'] == 'DPS']
        tanks = roster_priority_df[roster_priority_df['Role'] == 'Tank']['Raiders'].tolist()
        healers = roster_priority_df[roster_priority_df['Role'] == 'Healer']['Raiders'].tolist()

        # Calculate the total item upgrades for each DPS raider and add it as a new column
        dps_raiders['Total Upgrades'] = dps_raiders['Raiders'].apply(
            lambda raider: cls.total_item_upgrades_for_raider(raider,
                                                              'Broodkeeper Diurna',
                                                              droptimizer_data_difficulty_df))

        # Sort the DPS raiders DataFrame by priority (ascending) and then by total item upgrades (descending)
        dps_raiders = dps_raiders.sort_values(by=['Priority', 'Total Upgrades'], ascending=[True, False])

        # Initialize an empty dictionary to store raiders and their upgrade values
        roster_with_upgrades = {}
        bench_with_upgrades = {}

        # Add DPS raiders to the roster
        for _, row in dps_raiders.iterrows():
            raider = row['Raiders']
            total_upgrades = row['Total Upgrades']
            priority = row['Priority']

            # Split the character's name from their class
            character_name, _ = raider.split(' - ')

            # Check if the character is already in the roster
            character_already_in_roster = any(character_name in key for key in roster_with_upgrades.keys())

            if not character_already_in_roster:
                if len(roster_with_upgrades) < 14 and raider not in roster_with_upgrades:
                    if row['Priority'] == 1 and total_upgrades >= 100:
                        roster_with_upgrades[raider] = {"upgrades": total_upgrades, "priority": priority}
                    elif row['Priority'] == 1 and total_upgrades < 100:
                        # Find the next best raider to potentially replace the current raider
                        next_best_raider = dps_raiders.loc[dps_raiders['Priority'] > row['Priority']].iloc[0]
                        if next_best_raider['Total Upgrades'] > total_upgrades and next_best_raider[
                            'Raiders'] not in roster_with_upgrades:
                            roster_with_upgrades[next_best_raider['Raiders']] = {
                                "upgrades": next_best_raider['Total Upgrades'],
                                "priority": next_best_raider['Priority']}
                        else:
                            roster_with_upgrades[raider] = {"upgrades": total_upgrades, "priority": priority}
                    else:
                        roster_with_upgrades[raider] = {"upgrades": total_upgrades, "priority": priority}
                else:
                    bench_with_upgrades[raider] = {"upgrades": total_upgrades, "priority": priority}

        # Add Tanks and Healers to the roster_with_upgrades dictionary
        for tank in tanks:
            roster_with_upgrades[tank] = {"role": "Tank", "priority":
                roster_priority_df.loc[roster_priority_df['Raiders'] == tank, 'Priority'].values[0]}

        for healer in healers:
            roster_with_upgrades[healer] = {"role": "Healer", "priority":
                roster_priority_df.loc[roster_priority_df['Raiders'] == healer, 'Priority'].values[0]}

        print("Roster:", roster_with_upgrades)
        print("Bench:", bench_with_upgrades)


