import logging
import os
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.globals import set_debug, set_verbose


set_debug(True)
set_verbose(True)
logger = logging.getLogger(__name__)


class AgentBot:
    def __init__(self, parser: ParserTemplate, prompt: str, inputs: list[str], model_name: str, temperature,
                 max_tokens: int) -> None:
        self.parser = parser
        self.pydantic_parser = PydanticOutputParser(pydantic_object=parser)
        self.model_name = model_name
        self.prompt = prompt
        self.inputs = inputs
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = self.generate_model()
        self.prompt_template = self.generate_prompt_template()
        self.logger = logging.getLogger(self.__class__.__name__)

    def generate_model(self):
        return ChatOpenAI(
            model=os.environ['OPENAI_MODEL'],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            model_kwargs={'seed': 42},
            openai_api_key=os.environ['OPENAI_API_KEY'],
            verbose=True
        )

    def generate_prompt_template(self):
        return PromptTemplate(
            template=self.prompt,
            input_variables=self.inputs,
            partial_variables={"format_instructions": self.pydantic_parser.get_format_instructions()}
        )

    def run(self, input_variables: dict) -> Optional[object]:

        chain = self.prompt_template | self.model | self.pydantic_parser
        try:
            answer = chain.invoke(input_variables)
            # answer = self.run_fake_answer(ref)  # Use for simulate results

        except Exception as e:  # TODO use validation_error from pydantic
            self.logger.error("run :: --\n")
            self.logger.error(f"run :: Failed to invoke prompt {input_variables}")
            self.logger.error("run :: -- Error\n")
            self.logger.error(f"{e}")

        return answer


