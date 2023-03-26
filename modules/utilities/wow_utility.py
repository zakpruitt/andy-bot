import json

from discord import Colour


class WowUtility:

    @staticmethod
    def get_class_color(wow_class):
        with open('resources/class_color_map.json', 'r') as f:
            class_color_map = json.load(f)
        int_code = int(class_color_map[wow_class], 16)
        return Colour(int_code)

    @staticmethod
    def get_class_icon(wow_class):
        with open('resources/class_icon_map.json', 'r') as f:
            class_icon_map = json.load(f)
        return class_icon_map[wow_class]
