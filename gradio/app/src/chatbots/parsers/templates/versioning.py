import abc


class Versioning(abc.ABC):
    def __init__(self, parsers_list: list, index_main):
        self.parsers_list = parsers_list
        self.index_main = index_main
        self.main_parser = parsers_list[index_main]
