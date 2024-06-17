from typing import List

from langchain_core.pydantic_v1 import Field


class MissionV0(ParserTemplate):
    """Generate mission detailed from a description in French language."""

    context: str = Field(...,
                         description="the customer's needs in a general and succinct manner (only one short sentence maximum)")
    actions: List[str] = Field(
        ..., description="list where each element is a task to do for the mission described. One sentence per task"
    )
    technical_env: List[str] = Field(
        ...,
        description="lists the technical stack and tools used where each element of the list is a tecnical stack or a tool only with no explanation"
    )

    @staticmethod
    def generate_fields(context: str = "", actions=None, technical_env: list = None):
        return MissionV0(
            context=context,
            actions=actions if actions is not None else [],
            technical_env=technical_env if technical_env is not None else []
        )


class MissionV1(ParserTemplate):
    """Generate mission detailed from a description in French language."""

    context: str = Field(..., description="One short sentence to present the global context without presenting specific tasks.", examples=["Le projet vise à faire un audit interne pour le compte de Davidson.", "La mission consiste à créer des rapports PowerBI pour AXA."])
    actions: List[str] = Field(..., description="list where each element MUST BE a well structured and detailed phrase in present tense describing a task to do for the mission described.")
    technical_env: List[str] = Field(
        ..., description="lists the technical stack and tools used where each element of the list is a technical stack or a tool only with no explanation"
    )

    @staticmethod
    def generate_fields(context: str = "", actions=None, technical_env: list = None):
        return MissionV1(
            context=context,
            actions=actions if actions is not None else [],
            technical_env=technical_env if technical_env is not None else []
        )


PARSER_MISSION_LIST = Versioning([MissionV0, MissionV1], 0)
