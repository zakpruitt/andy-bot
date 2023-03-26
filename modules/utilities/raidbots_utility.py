import csv

import requests


class RaidbotsUtility:

    @staticmethod
    def get_report_csv(report_link):
        """ Downloads the Report Data from Raidbots using the Simple CSV data endpoint. """
        report_link = report_link + '/data.csv'

        with requests.Session() as s:
            raw_data = s.get(report_link)
        decoded_content = raw_data.content.decode('utf-8')
        csv_data = csv.reader(decoded_content.splitlines(), delimiter=',')
        data_list = list(csv_data)

        if "</Error>" in data_list[0][0]:
            return None
        return data_list
