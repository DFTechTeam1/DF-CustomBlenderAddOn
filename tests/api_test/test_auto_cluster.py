import httpx
import pytest
from src.secret import Config
from utils.error import LLMParserError
from src.schema.response import ResponseCluster3DModel

config = Config()


@pytest.mark.asyncio
async def test_cluster_3d_object_with_valid_payload():
    """Should return successfuly created cluster of 3D objects."""

    request_payload = {
        "object_name": [
            "wooden_table.001",
            "iron_gate.002",
            "mountain_peak.001",
            "robot_head.001",
            "fireplace.001",
        ],
        "temperature": 0.3,
    }

    async with httpx.AsyncClient(
        base_url=f"http://{config.IP_HOST}:{config.BACKEND_PORT}", timeout=300
    ) as client:
        response = await client.post("/auto/cluster-object", json=request_payload)
        response.status_code == 200
        api_res = response.json()
        assert api_res["data"] is not None


@pytest.mark.asyncio
async def test_cluster_3d_object_with_empty_object_payload() -> None:
    """Should raise InvalidOperationError when object_name is empty."""

    request_payload = {
        "object_name": [],
        "temperature": 0.3,
    }

    async with httpx.AsyncClient(
        base_url=f"http://{config.IP_HOST}:{config.BACKEND_PORT}", timeout=300
    ) as client:
        response = await client.post("/auto/cluster-object", json=request_payload)
        response.status_code == 400
        api_res = response.json()
        assert api_res["detail"] == "Input cannot be empty."


@pytest.mark.asyncio
async def test_cluster_3d_object_with_invalid_temperature_payload() -> None:
    """Should raise Unprocessable Entity when temperature is more than 1 or less than 0."""

    request_payload = {
        "object_name": ["wooden_table.001"],
        "temperature": 2,
    }

    async with httpx.AsyncClient(
        base_url=f"http://{config.IP_HOST}:{config.BACKEND_PORT}", timeout=300
    ) as client:
        response = await client.post("/auto/cluster-object", json=request_payload)
        response.status_code == 422


@pytest.mark.asyncio
async def test_cluster_3D_object_with_invalid_llm_response() -> None:
    """Should raise LLMParserError when Invalid LLM response."""
    mock_llm_response = {
        "Steampunk & Victorian": {
            "steampunk_airship": ["steampunk_building", "steampunk_lamp"]
        }
    }

    with pytest.raises(LLMParserError):
        ResponseCluster3DModel.validate_llm_response(data=mock_llm_response)


@pytest.mark.asyncio
async def test_cluster_3D_object_with_none_llm_response() -> None:
    """Should raise LLMParserError when LLM response format is None."""
    mock_llm_response = None
    with pytest.raises(LLMParserError):
        ResponseCluster3DModel.validate_llm_response(data=mock_llm_response)
