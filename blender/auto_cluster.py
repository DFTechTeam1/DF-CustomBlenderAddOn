import os
import bpy
import requests
import logging
from typing import Optional
from bpy.types import Operator, Panel
from collections import defaultdict


API_URL = os.getenv("API_URL", "http://192.168.99.28:10000/api/v1/auto/cluster-object")


BASE_FORMAT = "%(asctime)s %(levelname)s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=BASE_FORMAT,
    datefmt=DATE_FORMAT,
)


bl_info = {
    "name": "Auto Cluster Object",
    "category": "Development",
    "author": ("Bastian Armananta", "Edward"),
    "version": (1, 0, 0),
    "location": "View3D > Sidebar > Auto Cluster Object",
    "description": "A simple single-file Blender add-on",
}


class Preprocess:
    def unwrap(self) -> None:
        logging.info("Unwrapping all object into root collection.")
        scene = bpy.context.scene
        scene_collections = [collection for collection in scene.collection.children]
        for col in scene_collections:
            for obj in col.objects:
                scene.collection.objects.link(obj)
            scene.collection.children.unlink(col)

    def list_object(self, scene) -> list[str]:
        logging.info("Grab all object data.")
        object_names = [obj.name for obj in scene.objects]
        if not object_names:
            raise FileNotFoundError("No object data found in the current scene!")
        return object_names

    def to_lower(self, object_names: list[str]) -> list[str]:
        lowercased = [entry.lower() for entry in object_names]
        return lowercased

    def formatted_objects(self, scene) -> list:
        object_names = self.list_object(scene)
        processed_names = self.to_lower(object_names=object_names)
        return processed_names


class ResponseValidator:
    def validate_structure(
        self, response_api: dict, actual_objects: list
    ) -> Optional[dict]:
        validated_response = defaultdict(list)

        for key, values in response_api.items():
            for value in values:
                matches = [obj for obj in actual_objects if obj.startswith(value)]
                if matches:
                    validated_response[key].extend(matches)

        return dict(validated_response) if validated_response else None


class AutoClusterOperator(Operator):
    bl_idname = "object.auto_cluster"
    bl_label = "Auto Cluster Objects"

    def execute(self, context):
        scene = context.scene
        temperature = scene.cluster_temperature

        validator = ResponseValidator()

        preprocess = Preprocess()
        preprocess.unwrap()
        actual_objects = preprocess.formatted_objects(scene=scene)

        payload = {"object_name": actual_objects, "temperature": temperature}

        response = requests.post(
            API_URL, json=payload, headers={"Content-Type": "application/json"}
        )
        response_data = response.json()

        if response.status_code != 200:
            self.report({"ERROR"}, "LLM parsing error: Invalid response.")
            return {"CANCELLED"}

        clustered_data = response_data["data"]
        validated_response = validator.validate_structure(
            response_api=clustered_data, actual_objects=actual_objects
        )

        if not validated_response:
            self.report(
                {"ERROR"},
                "Object not found: LLM response and actial object is not satisfied.",
            )
            return {"CANCELLED"}

        for collection_name, objects in validated_response.items():
            new_collection = bpy.data.collections.new(collection_name)
            scene.collection.children.link(new_collection)

            for obj in scene.objects:
                obj_name = obj.name.lower()
                if obj_name in objects:
                    for collection in obj.users_collection:
                        collection.objects.unlink(obj)
                    new_collection.objects.link(obj)

        self.report({"INFO"}, "Objects successfully clustered!")
        return {"FINISHED"}


class AutoClusterPanel(Panel):
    bl_label = "Auto Cluster Object"
    bl_idname = "OBJECT_PT_auto_cluster"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Auto Cluster Object"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Clustering Options:")
        layout.prop(scene, "cluster_temperature", slider=True)
        layout.operator("object.auto_cluster", text="Cluster Objects")


classes = [AutoClusterOperator, AutoClusterPanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.cluster_temperature = bpy.props.FloatProperty(
            name="Temperature",
            description="Control clustering randomness",
            default=0.1,
            min=0.1,
            max=1.0,
        )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.cluster_temperature


if __name__ == "__main__":
    register()
