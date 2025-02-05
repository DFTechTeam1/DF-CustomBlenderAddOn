from ollama import Client
from src.secret import Config
from datetime import datetime
from pydantic import BaseModel
from utils.logger import logging
from utils.helper import local_time
from typing import Any, Union, Optional
from utils.error import ServiceError, LLMParserError
from langchain_core.prompts import PromptTemplate
from src.schema.response import ResponseCluster3DModel, ResponsePythonCodeGenerator
from src.schema.validator import LLMVResponseValidatorMixin

config = Config()

class CustomOllama:
    def __init__(
        self,
        model_name: str = "mistral:7b-instruct",
        temperature: float = 0.1,
    ):
        self.temperature: float = temperature
        self.model_name: str = model_name
        self.start_time: Optional[datetime] = None
        self.self_end_time: Optional[datetime] = None
        self.client = Client(host=config.OLLAMA_URL)

    def to_str(self, data: list) -> str:
        unique_values = set(data)
        convert_to_list = list(unique_values)
        logging.info(f"Clustering {len(convert_to_list)} unique object.")
        return str(convert_to_list)

    def prompt(self, custom_template: str, **kwargs: Any) -> str:
        prompt = PromptTemplate.from_template(template=custom_template)
        return prompt.format(**kwargs)

    def format_response(self, data: dict) -> dict:

        formatted_response = {}
        seen = set()

        for key, value in data.items():
            formatted_key = key.lower()
            formatted_key = formatted_key.replace(" ", "_") if " " in formatted_key else formatted_key
            formatted_value = []

            for entry in value:
                formatted_entry = entry.lower()
                formatted_entry = formatted_entry.replace(" ", "_") if " " in formatted_entry else formatted_entry

                if formatted_entry not in seen:
                    formatted_value.append(formatted_entry)
                    seen.add(formatted_entry)

            formatted_response[formatted_key] = formatted_value

        return formatted_response

    async def execute(
        self,
        custom_prompt: str,
        response_model: type[BaseModel],
    ) -> Union[dict, str]:
        try:
            self.start_time = local_time()
            logging.info("Starting LLM process.")

            response = self.client.chat(
                messages=[{"role": "user", "content": custom_prompt}],
                model=self.model_name,
                format=response_model.model_json_schema(),
                options={"temperature": self.temperature},
            )

            result = response_model.model_validate_json(response.message.content)

            if response_model is ResponsePythonCodeGenerator:
                response = LLMVResponseValidatorMixin.validate_response(
                    response=result.data.strip(), task_type="code"
                )
                return response
            elif response_model is ResponseCluster3DModel:
                response = LLMVResponseValidatorMixin.validate_response(
                    response=result.data, task_type="cluster"
                )
                response = self.format_response(data=response)
                return response
            else:
                raise ValueError("Unsupported response model type.")

        except LLMParserError:
            raise

        except Exception as e:
            logging.error(f"Error LLM: {e}")
            raise ServiceError(detail="Internal Service Error.")

        finally:
            self.end_time = local_time()
            logging.info("Finished LLM process.")
            logging.info(f"Elapsed time: {self.end_time-self.start_time}")
