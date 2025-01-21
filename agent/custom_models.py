import sys
from pathlib import Path
from ollama import chat

sys.path.append(str(Path(__file__).resolve().parents[1]))
from langchain_core.prompts import PromptTemplate
from agent.custom_template import organizer_template
from pydantic import BaseModel
from typing import Optional

from src.secret import Config

config = Config()


class ResponseDefault(BaseModel):
    data: Optional[dict] = None


object_data = [
    "statue.001",
    "statue_head.001",
    "rooftop.001",
    "watch.001",
    "watch.002",
    "chinesse_ornament.001",
    "chinesse_ornament.002",
    "tree.001",
    "tree.002",
    "tree.003",
]

prompt = PromptTemplate.from_template(template=organizer_template)
formatted_prompt = prompt.format(object_data=str(object_data))


response = chat(
    messages=[{"role": "user", "content": formatted_prompt}],
    model="llama3.2:3b-instruct-q2_K",
    format=ResponseDefault.model_json_schema(),
)

result = ResponseDefault.model_validate_json(response.message.content)
print(result)
