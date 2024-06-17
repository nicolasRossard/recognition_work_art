# TODO
# @abstract metho to_string etc
import json
from abc import ABC, abstractmethod

from langchain_core.pydantic_v1 import BaseModel


class ParserTemplate(BaseModel, ABC):
    def to_json(self) -> str:
        """Returns the JSON representation of the Mission instance."""
        return json.loads(self.json())

    def to_json_pretty(self) -> str:
        """Returns the pretty JSON representation of the Mission instance."""
        return json.dumps(json.loads(self.json()), ensure_ascii=False, indent=4)

    def to_string(self) -> str:
        return json.dumps(self.to_json(),  ensure_ascii=False)

    @staticmethod
    @abstractmethod
    def generate_fields():
        """ Generates empty fields for the parser"""
        pass
