import concurrent
import logging
import asyncio
import os
from collections import defaultdict

import pandas as pd

from apis.blizzard import Blizzard
from modules.embeds.droptimizer_search_embed import DroptimizerSearchEmbed
from modules.embeds.progress_embed import ProgressEmbed
from modules.parsers.droptimizer_parser import DroptimizerParser
from modules.utilities.google_sheets_utility import GoogleSheetsUtility


class DroptimizerService:
    sheet = GoogleSheetsUtility(os.getenv('DROPTIMIZER_SPREADSHEET_NAME'))

    @classmethod
    async def process_droptimizer_reports(cls, progress_embed, progress_msg):
        # get raider links
        raider_links = cls._gather_raider_links()
        progress_embed.advance_step()
        await progress_msg.edit(embed=progress_embed.get_embed())

        # parse reports
        mythic_reports, heroic_reports, normal_reports = await cls._parse_reports(raider_links)
        progress_embed.advance_step()
        await progress_msg.edit(embed=progress_embed.get_embed())

        # write reports to spreadsheet
        await cls._write_reports_to_spreadsheet(mythic_reports, heroic_reports, normal_reports)
        progress_embed.advance_step()
        await progress_msg.edit(embed=progress_embed.get_embed())
        logging.info('Droptimizer reports completed!')

    @classmethod
    def _gather_raider_links(cls):
        raiders = cls.sheet.Links.col_values(1)[1:]
        mythic_links = cls.sheet.Links.col_values(2)[1:]
        heroic_links = cls.sheet.Links.col_values(3)[1:]
        normal_links = cls.sheet.Links.col_values(4)[1:]
        raider_links = {}

        for raider, mythic, heroic, normal in zip(raiders, mythic_links, heroic_links, normal_links):
            raider_links[raider] = {
                'Mythic': mythic or None,
                'Heroic': heroic or None,
                'Normal': normal or None,
            }

        logging.info('Droptimizer data gathered.')
        return raider_links

    @classmethod
    async def _parse_reports(cls, raider_links):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            mythic_reports, heroic_reports, normal_reports = await loop.run_in_executor(executor,
                                                                                        DroptimizerParser.parse_reports,
                                                                                        raider_links)

        logging.info('Droptimizer reports parsed.')
        return mythic_reports, heroic_reports, normal_reports

    @classmethod
    async def _write_reports_to_spreadsheet(cls, mythic_reports, heroic_reports, normal_reports):
        data_frames = [pd.DataFrame(data=mythic_reports), pd.DataFrame(data=heroic_reports),
                       pd.DataFrame(data=normal_reports)]
        df = pd.concat(data_frames, keys=['Mythic', 'Heroic', 'Normal'])
        cls.sheet.write_data_to_worksheet('Data', df, include_index=True, include_column_header=True)
        logging.info('Droptimizer reports written to spreadsheet.')







    @staticmethod
    def get_boss_summary(data: dict):
        """ Grabs relevant statistics for each boss. """
        summary_data = defaultdict(lambda: {'player_count': 0, 'total': 0, 'max': 0, 'upgrade_count': 0})

        for player in data:
            upgraded_bosses = set()  # set to keep track of bosses that have been upgraded by the player

            # item = "Boss - Item", upgrade_value = float of dps increase
            for item, upgrade_value in data[player].items():
                boss_name = item.split('-')[0].strip()  # extract boss name

                # if the item is a significant upgrade, add it to the summary_data
                if upgrade_value > 100:
                    # check if the boss has been an upgrade before by the same player
                    if boss_name not in upgraded_bosses:
                        summary_data[boss_name]['player_count'] += 1
                        upgraded_bosses.add(boss_name)
                    summary_data[boss_name]['total'] += upgrade_value
                    summary_data[boss_name]['max'] = max(summary_data[boss_name]['max'], upgrade_value)
                    summary_data[boss_name]['upgrade_count'] += 1
        return dict(summary_data)

    @classmethod
    def search_droptimizer_data(cls, difficulty, search_type, search_string):
        try:
            worksheet = cls.sheet.get_worksheet(difficulty)
            dataframe = GoogleSheetsUtility.get_as_df(worksheet)

            dataframe.set_index('Boss', inplace=True)

            # Filter dataframe based on search string
            dataframe = dataframe[dataframe.index.str.contains(search_string, case=False)]
            dataframe = dataframe[dataframe > 0]

            # get max values for item and build new df
            max_values, max_items = dataframe.max(axis=0), dataframe.idxmax(axis=0)
            max_values = max_values.sort_values(ascending=False)
            result_df = pd.DataFrame({'Max Value': max_values, 'Item': max_items})
            result_df = result_df.dropna(how='all')
            result_df = result_df.sort_values(by="Max Value", ascending=False)

            embed = cls._get_item_search_embed(result_df, search_type)
            return embed
        except Exception as e:
            logging.error(e)
            return None

    @staticmethod
    def get_progress_embed():
        return ProgressEmbed(
            title=f'AotC Andy Droptimizer Report Processor',
            description='A new droptimizer report has been submitted! Please wait until the report has been processe' +
                        'd. This is indicated by all green checkmarks below.\n\n You can view the AotC Andy droptimi' +
                        'zer sheet [here](https://docs.google.com/spreadsheets/d/1LFUr61R9AewV3RDbIsz3Ibiivqm6IrISPl' +
                        '7QrZcF6XQ/edit#gid=1346039081).\n\n',
            steps_list=["Retrieve Droptimizer Reports", "Parse Droptimizer Reports", "Write Data"]
        )

    @staticmethod
    def _get_item_search_embed(result_df, search_type):
        if search_type == 'item':
            icon_name = result_df['Item'][0].split('-')[1].strip()
            icon_url = Blizzard.get_icon_from_item_name(icon_name)
        else:
            icon_name = result_df['Item'][0].split('-')[0].strip()
            icon_url = Blizzard.get_icon_from_boss_name(icon_name)

        return DroptimizerSearchEmbed(
            title=f'AotC Andy Droptimizer Search - {icon_name}',
            icon_url=icon_url,
            dataframe=result_df,
            search_type=search_type
        )

# # add boss summaries
        # cls.sheet.get_worksheet(difficulty).update('A1', 'Boss')
        # summary = DroptimizerService.get_boss_summary(data)
        # cls.sheet.write_data_to_worksheet('Summary',
        #                                   pd.DataFrame(data=summary).transpose().sort_index(),
        #                                   row=3,
        #                                   col=summary_col_idx[i - 2],
        #                                   include_index=i == 2,
        #                                   resize=False)