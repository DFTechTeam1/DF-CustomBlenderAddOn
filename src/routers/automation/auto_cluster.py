from fastapi import APIRouter
from utils.logger import logging
from agent.ollama import CustomOllama
from templates.prompt import cluster_template
from src.schema.request_format import AutoClusterRequest
from utils.error import ServiceError, BaseErrorCustomBlenderAddOn
from src.schema.response import ResponseDefault, ResponseCluster3DModel

router = APIRouter(tags=["Automation"], prefix="/auto")


async def auto_cluster_endpoint(schema: AutoClusterRequest) -> ResponseDefault:
    logging.info("Endpoint Auto Organize 3D Models.")
    response = ResponseDefault()
    ollama = CustomOllama(temperature=schema.temperature)

    try:
        formatted_data = ollama.to_str(data=schema.object_name).lower()
        print(formatted_data)
        formatted_prompt = ollama.prompt(
            custom_template=cluster_template, object_data=formatted_data
        )
        clustered_data = await ollama.execute(
            custom_prompt=formatted_prompt, response_model=ResponseCluster3DModel
        )

        response.message = "Success clustered 3D asset."
        response.data = clustered_data
    except BaseErrorCustomBlenderAddOn:
        raise
    except Exception as e:
        logging.error(f"Auto Cluster Error: {e}")
        raise ServiceError(detail="Internal Service Error.")
    return response


router.add_api_route(
    methods=["POST"],
    path="/cluster-object",
    endpoint=auto_cluster_endpoint,
    summary="Auto cluster 3D models collection.",
    response_model=ResponseDefault,
)
