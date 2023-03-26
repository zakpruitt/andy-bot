from apis.blizzard import Blizzard
from apis.dataclasses.sim import Sim
from modules.utilities.raidbots_utility import RaidbotsUtility


class DroptimizerParser:

    @staticmethod
    def parse_report(report):
        """ Parses the data in a raidbots data.csv to find the % increase for each sim reported. """
        base_dps = float(report[1][1])
        report_data = dict()

        # iterate through each sim and store max increases into data dict
        for raw_sim in report[2:]:
            sim = Sim(raw_sim[0], base_dps, float(raw_sim[1]))

            item_name = f"{Blizzard.get_boss_from_id(sim.boss_id)[0]} - {Blizzard.get_item_from_id(sim.item_id)[0]}"
            if item_name in report_data:
                report_data[item_name] = max(sim.sim_difference, report_data[item_name])
            else:
                report_data[item_name] = sim.sim_difference

        # return player ([1][0]) and report data
        return report_data

    @staticmethod
    def parse_reports(report_list, player_list):
        parsed_reports = {}
        if len(report_list) > 0:
            for i in range(len(report_list)):
                report_link = report_list[i]
                report_data = RaidbotsUtility.get_report_csv(report_link)
                if report_data is None:
                    raise Exception("Report link is invalid! Report link violated: " + report_link + ".")
                data = DroptimizerParser.parse_report(report_data)
                parsed_reports[player_list[i]] = data
        return parsed_reports
