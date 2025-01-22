from fastapi import APIRouter
from utils.logger import logging
from agent.ollama import CustomOllama
from src.schema.response import ResponseDefault
from templates.prompt import organizer_template
from src.schema.request_format import ModelData
from utils.error import ServiceError, BaseErrorCustomBlenderAddOn

router = APIRouter(tags=["Automation"], prefix="/auto")


async def auto_organize_endpoint(schema: ModelData) -> ResponseDefault:
    logging.info("Endpoint Auto Organize 3D Models.")
    response = ResponseDefault()
    ollama = CustomOllama(temperature=0.15)

    try:
        formatted_data = ollama.to_str(data=schema.model)
        formatted_prompt = ollama.prompt(
            custom_template=organizer_template, object_data=formatted_data
        )
        clustered_data = await ollama.cluster_models(custom_prompt=formatted_prompt)

        response.message = "Success clustered 3D asset."
        response.data = clustered_data
    except BaseErrorCustomBlenderAddOn:
        raise
    except Exception:
        raise ServiceError(detail="Internal Service Error.")
    return response


router.add_api_route(
    methods=["POST"],
    path="/cluster-object",
    endpoint=auto_organize_endpoint,
    summary="Auto Organize 3D Models Collection.",
    response_model=ResponseDefault,
)
