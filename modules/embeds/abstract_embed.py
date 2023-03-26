from abc import ABC, abstractmethod


class AbstractEmbed(ABC):

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_embed(self):
        pass

    @abstractmethod
    def error(self):
        pass

    def add_field_line_break(self, embed):
        embed.add_field(name="\u200B", value="\u200B", inline=False)
