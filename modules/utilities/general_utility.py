import datetime
import time


class GeneralUtility:

    @staticmethod
    def get_time_and_date():
        today_var = datetime.date.today()
        time_var = time.strftime("%I:%M %p")
        date_var = today_var.strftime("%m/%d/%y")
        return time_var, date_var
