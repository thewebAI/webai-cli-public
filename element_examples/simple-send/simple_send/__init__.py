import asyncio
from typing import AsyncIterator
from uuid import UUID
import numpy as np

from webai_element_sdk.element.settings import ElementSettings, TextSetting, NumberSetting, equals
from webai_element_sdk.comms.messages import ColorFormat, ImageFrame, RegionOfInterest, SegmentationMask
from webai_element_sdk.element import Context, Element
from webai_element_sdk.element.variables import ElementOutputs, Output


class Outputs(ElementOutputs):
    default = Output[ImageFrame]()


class Settings(ElementSettings):
    color = TextSetting(
        name="color",
        display_name="Color",
        default="black",
        valid_values=["black", "red", "green", "blue"]
    )
    delay = NumberSetting[int](
        name="delay",
        display_name="Delay",
        default=50,
        hints=["advanced"],
        depends_on=equals("color", "red")
    )


element = Element(
    id=UUID("74040ed5-9440-423c-8541-5155aef24338"),
    name="simple_send",
    display_name="Simple Send",
    version="0.1.0",
    framework_version="0.7",
    settings=Settings(),
    outputs=Outputs(),
)

colors = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}


@element.executor
async def simple_send(
    ctx: Context[None, Outputs, Settings]
) -> AsyncIterator[Output[ImageFrame]]:
    """Simple Send"""

    img = np.zeros(shape=(1080, 1920, 3), dtype=np.uint8)
    img[:, :] = colors[ctx.settings.color.value]
    
    binary_mask = np.zeros(shape=(1080, 1920), dtype=np.uint8)
    mask_height = 100
    mask_width = 200
    start_row = np.random.randint(0, 1080 - mask_height + 1)
    start_col = np.random.randint(0, 1920 - mask_width + 1)
    binary_mask[start_row:start_row + mask_height, start_col:start_col + mask_width] = 1
    
    mask = SegmentationMask(binary_mask)
    rois = [
        RegionOfInterest(0, 0, img.shape[1], img.shape[0], [], mask)
    ]
    frame = ImageFrame(img, rois, ColorFormat.RGB)

    while True:
        yield ctx.outputs.default(frame)
        if ctx.settings.delay.value > 0:
            await asyncio.sleep(ctx.settings.delay.value / 1000)
