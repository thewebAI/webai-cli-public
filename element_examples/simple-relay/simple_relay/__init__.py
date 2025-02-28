from typing import AsyncIterator
from uuid import UUID

import numpy as np
from webai_element_sdk.comms.messages import ImageFrame
from webai_element_sdk.element import Context, Element
from webai_element_sdk.element.variables import ElementInputs, ElementOutputs, Input, Output


class Inputs(ElementInputs):
    default = Input[ImageFrame]()


class Outputs(ElementOutputs):
    default = Output[ImageFrame]()


element = Element(
    id=UUID("ae601581-d71f-46f1-b31b-4883d56ec854"),
    name="simple_relay",
    display_name="Simple Relay",
    version="0.1.0",
    framework_version="0.9",
    inputs=Inputs(),
    outputs=Outputs(),
    is_inference=True,
)
idx = 0
y_offset_factor = np.random.uniform(0.25, 0.75)


@element.executor
async def simple_relay(
    ctx: Context[Inputs, Outputs, None]
) -> AsyncIterator[Output[ImageFrame]]:
    """Simple Relay"""
    global idx

    frame = ctx.inputs.default.value
    img = frame.ndframe.copy()
    if len(frame.rois) > 0:
        binary_mask = frame.rois[0].mask.binary_mask
        img[binary_mask.astype(bool)] = [100, 100, 100]

    box_size = 50
    box_color = (255, 255, 255)
    box_border_width = 3
    box_speed = 1
    idx = (idx + box_speed) % (img.shape[1])
    y_offset = y_offset_factor * img.shape[0]
    y_pos_long_arc = (img.shape[0] * 0.18) * np.sin(2 * np.pi * idx / img.shape[1])
    y_pos_short_arc = (img.shape[0] * 0.05) * np.cos(idx * 0.03)
    y_pos = int(y_pos_long_arc + y_pos_short_arc + y_offset)
    img[y_pos: (y_pos + box_size), idx: idx + box_size] = box_color
    img[
        y_pos + box_border_width: (y_pos + box_size - box_border_width),
        idx + box_border_width: idx + box_size - box_border_width,
    ] = (0, 0, 0)
    
    frame.ndframe = img
    
    yield ctx.outputs.default(frame)

