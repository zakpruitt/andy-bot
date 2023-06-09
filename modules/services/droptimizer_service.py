import asyncio
import concurrent
import logging
import os
import re
from itertools import zip_longest

import numpy as np
import pandas as pd

from apis.blizzard_api import BlizzApi
from modules.embeds.droptimizer_search_embed import DroptimizerSearchEmbed
from modules.embeds.progress_embed import ProgressEmbed
from modules.parsers.droptimizer_parser import DroptimizerParser
from modules.utilities.google_sheets_utility import GoogleSheetsUtility
from modules.utilities.raidbots_utility import RaidbotsUtility


class DroptimizerService:
    sheet = GoogleSheetsUtility(os.getenv('DROPTIMIZER_SPREADSHEET_NAME'))
    DROPTIMIZER_REPORTS_URL_PATTERN = r'https://www\.raidbots\.com/simbot/report/[a-zA-Z0-9]+'
    DROPTIMIZER_DIFFICULTY_PATTERN = r'\b(Mythic|Heroic|Normal)\b$'

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

    @staticmethod
    def get_progress_embed():
        return ProgressEmbed(
            title=f'AotC Andy Droptimizer Report Processor',
            description='A new droptimizer report has been submitted! Please wait until the report has been processe' +
                        'd. This is indicated by all green checkmarks below.\n\n You can view the AotC Andy droptimi' +
                        'zer sheet [here](https://docs.google.com/spreadsheets/d/1LFUr61R9AewV3RDbIsz3Ibiivqm6IrISPl' +
                        '7QrZcF6XQ/edit#gid=1346039081).',
            steps_list=["Retrieve Droptimizer Reports", "Parse Droptimizer Reports", "Write Data"]
        )

    @classmethod
    def _gather_raider_links(cls):
        raiders = cls.sheet.Links.col_values(1)[1:]
        mythic_links = cls.sheet.Links.col_values(2)[1:]
        heroic_links = cls.sheet.Links.col_values(3)[1:]
        normal_links = cls.sheet.Links.col_values(4)[1:]
        raider_links = {}

        for raider, mythic, heroic, normal in zip_longest(raiders, mythic_links, heroic_links, normal_links):
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
        # create dataframe from reports
        data_frames = (pd.DataFrame(data=d) for d in [mythic_reports, heroic_reports, normal_reports])
        df = pd.concat(data_frames, keys=['Mythic', 'Heroic', 'Normal']).reset_index(level=1)

        # process dataframe
        result_df = cls._process_dataframe(df)
        result_df = result_df.pivot_table(index=['Difficulty', 'Boss', 'Item'], columns='Player', values='Value',
                                          aggfunc='first').reset_index()

        # write dataframe to spreadsheet
        cls.sheet.write_data_to_worksheet('Data', result_df, include_index=False, include_column_header=True)
        logging.info('Droptimizer reports written to spreadsheet.')

    @staticmethod
    def _process_dataframe(df):
        df_item_values = df.apply(lambda x: x.apply(
            lambda y: pd.DataFrame(y.items(), columns=['Item', 'Value']) if isinstance(y, dict) else y))
        result_df = pd.concat(
            [row[col].assign(Difficulty=idx, Boss=row[0], Player=col) for col in df_item_values.columns
             for idx, row in df_item_values.iterrows() if isinstance(row[col], pd.DataFrame)], ignore_index=True)
        return result_df

    @classmethod
    def search_droptimizer_data(cls, difficulty, search_type, search_string):
        try:
            # get dataframe from spreadsheet
            worksheet = cls.sheet.get_data_worksheet()
            dataframe = GoogleSheetsUtility.get_as_df(worksheet)

            # filter dataframe based on difficulty and search string
            dataframe = dataframe.loc[dataframe['Difficulty'] == difficulty]
            if search_type == 'item':
                dataframe = dataframe[dataframe['Item'].str.contains(search_string, case=False)]
            else:
                dataframe = dataframe[dataframe['Boss'].str.contains(search_string, case=False)]
            dataframe = dataframe.applymap(lambda x: np.nan if isinstance(x, (int, float)) and x < 0 else x)
            dataframe.dropna(how='all', axis='columns', inplace=True)

            # set index and drop unneeded columns
            dataframe.set_index(['Boss', 'Item'], inplace=True)
            dataframe.drop('Difficulty', axis=1, inplace=True)

            # get max values for item and build new df
            max_values, max_items = dataframe.max(axis=0), dataframe.idxmax(axis=0)

            # combine max values, items, and boss names
            result_df = pd.DataFrame({
                'Max Value': max_values,
                'Item': [boss_item_tuple[1] for boss_item_tuple in max_items],
                'Boss': [boss_item_tuple[0] for boss_item_tuple in max_items],
            })
            result_df.sort_values(by="Max Value", ascending=False, inplace=True)

            # build search embed and return
            embed = cls._get_item_search_embed(result_df, search_type)
            return embed
        except Exception as e:
            logging.error(e)
            return None

    @staticmethod
    def _get_item_search_embed(result_df, search_type):
        if search_type == 'item':
            icon_name = result_df['Item'][0]
            icon_url = BlizzApi.get_icon_from_item_name(icon_name)
        else:
            icon_name = result_df['Boss'][0]
            icon_url = BlizzApi.get_icon_from_boss_name(icon_name)

        return DroptimizerSearchEmbed(
            title=icon_name,
            icon_url=icon_url,
            dataframe=result_df,
            search_type=search_type
        )

    @classmethod
    async def add_droptimizer_report(cls, message):
        # get links
        links_sheet = cls.sheet.get_worksheet('Links')
        links = re.findall(cls.DROPTIMIZER_REPORTS_URL_PATTERN, message)

        # add to sheet
        for link in links:
            name_spec, difficulty = cls.__get_droptimizer_link_info(link)
            player = links_sheet.find(name_spec)

            if player is None:
                row_num = len(links_sheet.col_values(1)) + 1
                links_sheet.update_cell(row_num, 1, name_spec)
            else:
                row_num = player.row

            if difficulty == "Mythic":
                links_sheet.update_cell(row_num, 2, link)
            elif difficulty == "Heroic":
                links_sheet.update_cell(row_num, 3, link)
            elif difficulty == "Normal":
                links_sheet.update_cell(row_num, 4, link)

        return len(links)

    @staticmethod
    def __get_droptimizer_link_info(link):
        report_data = RaidbotsUtility.get_report_json(link)
        if report_data['simbot']['simType'] != 'droptimizer':
            raise Exception(f'Report {link} is not a droptimizer report!')
        name_spec = f"{report_data['simbot']['player']} - {report_data['simbot']['spec'].capitalize()}"
        difficulty = report_data['simbot']['publicTitle'].split('•')[-1].strip()
        return name_spec, difficulty
