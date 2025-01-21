import sys
from pathlib import Path
import ollama

sys.path.append(str(Path(__file__).resolve().parents[1]))
from langchain_core.prompts import PromptTemplate
from custom_template import organizer_template

formatted_object_data = str(
    [
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
)
prompt = PromptTemplate.from_template(template=organizer_template)
formatted_prompt = prompt.format(object_data=formatted_object_data)

response = ollama.generate(model="mistral:7b-instruct", prompt=formatted_prompt)

print(response["response"])
