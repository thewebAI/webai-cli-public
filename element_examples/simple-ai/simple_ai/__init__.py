from uuid import UUID

from webai_element_sdk.element import Element

import simple_ai.train as trainer
import simple_ai.inference as predictor

element = Element(
    id=UUID("76d615a1-66bd-4577-b621-c7d7926ac699"),
    name="simple_ai",
    display_name="Simple AI",
    version="0.1.0",
    sub_elements=[
        trainer.element,
        predictor.element,
    ],
)
