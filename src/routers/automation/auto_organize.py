from fastapi import APIRouter
from utils.logger import logging
from src.schema.response import ResponseDefault
from src.schema.request_format import ModelData

router = APIRouter(tags=["Automation"], prefix="/auto")


async def auto_organize_endpoint(schema: ModelData) -> ResponseDefault:
    logging.info("Endpoint Auto Organize 3D Models.")
    response = ResponseDefault()
    return response


router.add_api_route(
    methods=["POST"],
    path="/cluster-object",
    endpoint=auto_organize_endpoint,
    summary="Auto Organize 3D Models Collection.",
    response_model=ResponseDefault,
)
