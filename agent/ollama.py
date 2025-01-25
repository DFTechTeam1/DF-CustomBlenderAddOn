from ollama import chat
from typing import Any, Union
from pydantic import BaseModel
from utils.logger import logging
from utils.helper import local_time
from utils.error import ServiceError
from langchain_core.prompts import PromptTemplate
from src.schema.response import ResponseCluster3DModel, ResponsePythonCodeGenerator


class CustomOllama:
    def __init__(
        self,
        model_name: str = "mistral:7b-instruct",
        temperature: float = 0.1,
    ):
        self.temperature = temperature
        self.model_name = model_name
        self.start_time = None
        self.self_end_time = None

    def to_str(self, data: list) -> str:
        logging.info(f"Clustering {len(data)} object.")
        return str(data)

    def prompt(self, custom_template: str, **kwargs: Any) -> str:
        prompt = PromptTemplate.from_template(template=custom_template)
        return prompt.format(**kwargs)

    async def execute(
        self,
        custom_prompt: str,
        response_model: type[BaseModel],
    ) -> Union[dict, str]:
        try:
            self.start_time = local_time()
            logging.info("Starting LLM process.")

            response = chat(
                messages=[{"role": "user", "content": custom_prompt}],
                model=self.model_name,
                format=response_model.model_json_schema(),
                options={"temperature": self.temperature},
            )

            result = response_model.model_validate_json(response.message.content)

            if response_model is ResponsePythonCodeGenerator:
                return result.data.strip()
            elif response_model is ResponseCluster3DModel:
                return result.data
            else:
                raise ValueError("Unsupported response model type.")

        except Exception as e:
            logging.error(f"Error LLM: {e}")
            raise ServiceError(detail="Internal Service Error.")

        finally:
            self.end_time = local_time()
            logging.info("Finished LLM process.")
            logging.info(f"Elapsed time: {self.end_time-self.start_time}")
