import datetime
import json
import os
import time


class GeneralUtility:

    @staticmethod
    def get_time_and_date():
        today_var = datetime.date.today()
        time_var = time.strftime("%I:%M %p")
        date_var = today_var.strftime("%m/%d/%y")
        return time_var, date_var

    @staticmethod
    def get_spec_abbreviation(character_spec):
        with open(os.getenv("BOT_PATH") + 'resources/spec_abbrv_map.json', 'r') as spec_abbrv_map:
            name, spec = character_spec.split(" - ")
            abbreviation = json.load(spec_abbrv_map)[spec.lower()]
            return f"{name} - {abbreviation}"
