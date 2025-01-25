import httpx
import pytest


@pytest.mark.asyncio
async def test_crete_cluster_3d_object():
    async with httpx.AsyncClient(
        base_url="http://localhost:8000", timeout=300
    ) as client:
        request_payload = {
            "model": [
                "wooden_table.001",
                "iron_gate.002",
                "mountain_peak.001",
                "robot_head.001",
                "fireplace.001",
                "stone_bench.001",
                "medieval_sword.001",
                "flying_car.001",
                "jungle_tree.001",
                "treasure_chest.001",
                "viking_shield.001",
                "desert_dune.001",
                "stone_tower.001",
                "fire_bowl.001",
                "waterfall.001",
                "rock_formation.001",
                "wooden_chair.001",
                "glowing_plant.001",
                "metallic_door.001",
                "ancient_pillar.001",
                "candle_stand.001",
                "futuristic_vehicle.001",
                "skyscraper.001",
                "flying_drones.001",
                "castle_wall.001",
                "medieval_castle.001",
            ],
            "temperature": 0.3,
        }

        response = await client.post("/auto/cluster-object", json=request_payload)
        response.status_code == 200
