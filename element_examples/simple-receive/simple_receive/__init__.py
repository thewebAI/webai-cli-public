import asyncio
import pathlib
from typing import AsyncIterator, Set
from uuid import UUID

from webai_element_sdk import Context, Element
from webai_element_sdk.comms.messages import ImageFrame, Preview
from webai_element_sdk.element.variables import ElementInputs, ElementOutputs, Input, Output
from quart import Quart, Response, render_template, jsonify
from quart_cors import route_cors

from .interface import generate_image_from_frame


class Inputs(ElementInputs):
    default = Input[AsyncIterator[ImageFrame]]()


class Outputs(ElementOutputs):
    preview = Output[Preview]()


element = Element(
    id=UUID("9ebdfcbb-2dbb-4c67-aa6b-02820feb55d9"),
    name="simple_receive",
    display_name="Simple Receive",
    version="0.3.0",
    framework_version="0.6",
    inputs=Inputs(),
    outputs=Outputs(),
)
template_path = str((pathlib.Path(__file__).parent / "deps").resolve())
app = Quart(__name__, template_folder=template_path)


class FrameBroadcaster:
    def __init__(self):
        self.clients: Set[asyncio.Queue] = set()

    async def add_client(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self.clients.add(queue)
        return queue

    async def remove_client(self, queue: asyncio.Queue):
        self.clients.remove(queue)

    async def broadcast(self, frame):
        for queue in self.clients:
            await queue.put(frame)


broadcaster = FrameBroadcaster()


@app.route("/config")
@route_cors(
    allow_headers=["content-type"],
    allow_methods=["GET"],
    allow_origin=["*"],
)
async def config():
    return jsonify({
        "type": "preview",
        "endpoint": "/image"
    })


@app.route("/image")
async def get_image():
    async def receive_frames():
        queue = await broadcaster.add_client()
        try:
            while True:
                frame = await queue.get()
                yield frame
        finally:
            await broadcaster.remove_client(queue)

    response = Response(
        receive_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

    response.timeout = None
    return response


@app.route("/")
async def index():
    return await render_template("index.html")


@element.startup
async def startup(ctx: Context[Inputs, Outputs, None]):
    await ctx.logger.log("Starting Element: Multi-client Receive")
    
    # Start the Quart app
    asyncio.create_task(app.run_task(host="0.0.0.0", port=ctx.preview_port, debug=False))


@element.executor
async def run(ctx: Context[Inputs, Outputs, None]):
    async def frame_reader():
        async for frame in ctx.inputs.default.value:
            await broadcaster.broadcast(generate_image_from_frame(frame))

    await frame_reader()  # This will run for the lifetime of the element
