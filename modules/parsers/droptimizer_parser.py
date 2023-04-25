from apis.blizzard_api import BlizzApi
from apis.dataclasses.sim import Sim
from modules.utilities.raidbots_utility import RaidbotsUtility


class DroptimizerParser:

    @staticmethod
    def parse_report(report):
        base_dps = float(report[1][1])
        report_data = {}

        # iterate through each sim and store max increases into data dict
        for raw_sim in report[2:]:
            # gather data
            sim = Sim(raw_sim[0], base_dps, float(raw_sim[1]))
            boss_name = BlizzApi.get_boss_from_id(sim.boss_id)[0]
            item_name = BlizzApi.get_item_from_id(sim.item_id)[0]

            # check if boss name is in data dict
            if boss_name not in report_data:
                report_data[boss_name] = {}

            # add max sim for item to data dict
            if item_name in report_data[boss_name]:
                report_data[boss_name][item_name] = max(sim.sim_difference, report_data[boss_name][item_name])
            else:
                report_data[boss_name][item_name] = sim.sim_difference

        return report_data

    @staticmethod
    def parse_reports(raider_links):
        parsed_reports = {difficulty: {} for difficulty in ["Mythic", "Heroic", "Normal"]}

        for raider, links in raider_links.items():
            for difficulty in ["Mythic", "Heroic", "Normal"]:
                link = links.get(difficulty)
                if link is not None:
                    report_data = RaidbotsUtility.get_report_csv(link)
                    if report_data is None:
                        raise Exception("Report link is invalid! Report link violated: " + link + ".")
                    parsed_reports[difficulty][raider] = DroptimizerParser.parse_report(report_data)

        return parsed_reports["Mythic"], parsed_reports["Heroic"], parsed_reports["Normal"]
