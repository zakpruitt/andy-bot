import os

from apis.raider_io_api import RaiderIoApi
from modules.utilities.google_sheets_utility import GoogleSheetsUtility


class RosterService:
    sheet = GoogleSheetsUtility(os.getenv('DROPTIMIZER_SPREADSHEET_NAME'))

    @staticmethod
    def a():
        prog = RaiderIoApi.get_guild_current_raid_progression()
        print(prog)
