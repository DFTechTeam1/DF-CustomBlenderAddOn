from fastapi import APIRouter
from utils.logger import logging
from agent.ollama import CustomOllama
from src.schema.request_format import UserPrompt
from templates.prompt import code_generator_template
from utils.error import ServiceError, BaseErrorCustomBlenderAddOn
from src.schema.response import ResponseDefault, ResponsePythonCodeGenerator

router = APIRouter(tags=["Automation"], prefix="/auto")


async def code_generator_endpoint(schema: UserPrompt) -> ResponseDefault:
    logging.info("Endpoint Auto Generate Python Code.")
    response = ResponseDefault()
    ollama = CustomOllama(temperature=schema.temperature)

    try:
        formatted_prompt = ollama.prompt(
            custom_template=code_generator_template, user_prompt=schema.prompt
        )
        custom_code = await ollama.execute(
            custom_prompt=formatted_prompt, response_model=ResponsePythonCodeGenerator
        )

        response.message = "Success generated python code."
        response.data = custom_code
    except BaseErrorCustomBlenderAddOn:
        raise
    except Exception:
        raise ServiceError(detail="Internal Service Error.")
    return response


router.add_api_route(
    methods=["POST"],
    path="/code-generator",
    endpoint=code_generator_endpoint,
    summary="Auto generate python code.",
    response_model=ResponseDefault,
)
