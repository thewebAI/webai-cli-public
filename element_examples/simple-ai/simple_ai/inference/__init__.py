from uuid import UUID
from pathlib import Path
import json
from webai_element_sdk.element import Element, Context
from webai_element_sdk.element.settings import (
    ElementSettings,
    generate_artifact_setting,
)
from simple_ai.model import Model

# This will expose a dropdown of artifacts in Navigator to select from registered model artifacts
# This will tell Runtime to pull the artifact to the node running this element, unzip it, and make it available in the current working directory.
class Settings(ElementSettings):
    artifact = generate_artifact_setting(False)

element = Element(
    id=UUID("8d59c59f-86bc-4f38-b132-4b5e07fb265f"),
    name="inference",
    display_name="Simple AI Predictor",
    is_inference=True,
    settings=Settings(),
)

@element.startup
async def startup(ctx: Context[None, None, Settings]):
    global model
    
    # Step 1: Get the current working directory
    current_directory = Path.cwd()

    # Step 2: Create a folder named "artifact"
    artifact_path = current_directory / "artifact"
    artifact_path.mkdir(exist_ok=True)

    # Step 3: Get metadata.json file within "artifact" with some sample fields
    expected_metadata = {
        "name": "Sample Artifact",
        "version": "1.0",
        "description": "This is a sample metadata file.",
    }
    metadata_path = artifact_path / "metadata.json"
    with metadata_path.open(mode="r") as metadata_file:
        actual_metadata = json.load(metadata_file)
        assert actual_metadata == expected_metadata, f"Expected {expected_metadata}, but got {actual_metadata}"
        print("Metadata:", actual_metadata)


    # Step 4: Get a text file within "artifact" that says "hello world"
    artifact_path = artifact_path / "model.txt"
        
    # Step 5: In real use-case pass the artifact path to your model to load once at startup
    model = Model().load(artifact_path)


@element.executor
async def simple_predictor(ctx: Context[None, None, None]):
    """Simple Element"""
    inference = model.predict(123)
    # then send this out to the next element (see simple-send/relay examples)
