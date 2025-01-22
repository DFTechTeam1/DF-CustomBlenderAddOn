from ollama import chat
from datetime import datetime
from utils.logger import logging
from typing import Optional, Any
from utils.helper import local_time
from utils.error import ServiceError
from langchain_core.prompts import PromptTemplate
from src.schema.response import ResponseLLM


class CustomOllama:
    def __init__(
        self,
        model_name: str = "mistral:7b-instruct",
        temperature: float = 0.1,
    ):
        self.temperature = temperature
        self.model_name = model_name
        self.start_time: Optional[datetime] = None
        self.self_end_time: Optional[datetime] = None

    def to_str(self, data: list) -> str:
        return str(data)

    def prompt(self, custom_template: str, **kwargs: Any) -> str:
        prompt = PromptTemplate.from_template(template=custom_template)
        return prompt.format(**kwargs)

    async def cluster_models(self, custom_prompt: str) -> dict:
        try:
            start_time = local_time()
            logging.info("Starting clustering process.")

            response = chat(
                messages=[{"role": "user", "content": custom_prompt}],
                model=self.model_name,
                format=ResponseLLM.model_json_schema(),
                options={"temperature": self.temperature},
            )

            result = ResponseLLM.model_validate_json(response.message.content)

            end_time = local_time()
            logging.info("Finished clustering proceess.")
            logging.info(f"Elapsed time: {end_time-start_time}")
        except Exception as e:
            logging.error(f"Error clustering 3D models: {e}")
            raise ServiceError(detail="Internal Service Error.")

        return result.data
