import abc


class Versioning(abc.ABC):
    def __init__(self, prompts_list: list, index_main):
        self.prompts_list = prompts_list
        self.index_main = index_main
        self.main_prompt = prompts_list[index_main]
