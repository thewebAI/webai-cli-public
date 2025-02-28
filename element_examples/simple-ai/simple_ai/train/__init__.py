import time
from typing import Any, Dict
from uuid import UUID
from pathlib import Path
import json
from webai_element_sdk.element import Element, Context
from simple_ai.model import Model

element = Element(
    id=UUID("72a0a0c5-86ed-46a9-88d3-aa75acd51286"),
    name="train",
    display_name="Simple AI Trainer",
    is_training=True,
    training_metrics_schema={
        "accuracy": {
            "title": "Accuracy",
            "xLabel": "Epochs",
            "yLabels": {
                "train": "Train",
                "validation": "Validation"
            }
        },
        "loss": {
            "title": "Loss",
            "xLabel": "Epochs",
            "yLabels": {
                "train": "Train",
                "validation": "Validation"
            }
        }
    },
)


@element.executor
async def simple_trainer(ctx: Context[None, None, None]):
    """Simple Element"""

    # This is how metrics get passed to DB and MQTT to be seen in Navigator
    def callback(metrics: Dict[str, Any]):
        ctx.logger.update_training_metrics(metrics)
    
    # In real use-case, define a setting for this trainer element to pass in a dataset path
    model = Model()
    model.train(5, callback)

    # Step 1: Get the current working directory
    current_directory = Path.cwd()

    # Step 2: Create a folder named "artifact"
    artifact_path = current_directory / "artifact"
    artifact_path.mkdir(exist_ok=True)

    # Step 3: Create a metadata.json file within "artifact" with some sample fields
    metadata = {
        "name": "Sample Artifact",
        "version": "1.0",
        "description": "This is a sample metadata file.",
    }
    metadata_path = artifact_path / "metadata.json"
    with metadata_path.open(mode="w") as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

    # Step 4: Create a text file within "artifact" that says "hello world"
    hello_world_path = artifact_path / "model.txt"
    hello_world_content = "hello world"
    hello_world_path.write_text(hello_world_content)
