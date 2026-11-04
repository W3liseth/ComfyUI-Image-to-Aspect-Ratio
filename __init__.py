import math

import nodes
from comfy_api.latest import ComfyExtension, io


WEB_DIRECTORY = "./web"

ASPECT_RATIOS = [
    "1:1 (Square)",
    "2:3 (Portrait Photo)",
    "3:2 (Photo)",
    "3:4 (Portrait Standard)",
    "4:3 (Standard)",
    "9:16 (Portrait Widescreen)",
    "16:9 (Widescreen)",
    "21:9 (Ultrawide)",
    "Custom",
]


def resolution(megapixels, multiple, width, height):
    if not all(math.isfinite(v) and v > 0 for v in (megapixels, width, height)):
        raise ValueError("Megapixels and aspect ratio values must be finite and positive.")
    if multiple < 1:
        raise ValueError("Multiple must be a positive integer.")
    grid = math.lcm(multiple, 8)
    ratio = width / height
    target_height = math.sqrt(megapixels * 1024 * 1024 / ratio)
    width = max(grid, math.floor(target_height * ratio / grid + 0.5) * grid)
    height = max(grid, math.floor(target_height / grid + 0.5) * grid)
    return width, height


class AspectRatioEmptyLatent(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="AspectRatioEmptyLatent",
            display_name="Image to aspect ratio",
            category="latent",
            description="Create a standard empty latent using the image's aspect ratio, or a manual ratio when no image is connected.",
            inputs=[
                io.Image.Input("image", optional=True, tooltip="Uses the actual width/height ratio, preserving portrait or landscape orientation."),
                io.Combo.Input("aspect_ratio", options=ASPECT_RATIOS, default="4:3 (Standard)", tooltip="Used only when no image is connected."),
                io.Float.Input("megapixels", default=1.0, min=0.01, max=64.0, step=0.01, tooltip="Target pixel area: 1 MP = 1024 × 1024 pixels. Rounded dimensions may change the final area slightly."),
                io.Int.Input("multiple", default=32, min=1, max=4096, step=1, tooltip="Dimensions are rounded to a multiple of this value and 8, as required by the standard latent."),
                io.String.Input("custom_ratio", default="4:3", tooltip="Used with Custom. Enter width:height, for example 5:7 or 1.85:1.", advanced=True),
                io.Int.Input("batch_size", default=1, min=1, max=4096, advanced=True),
            ],
            outputs=[
                io.Latent.Output(display_name="latent"),
                io.Int.Output(display_name="width"),
                io.Int.Output(display_name="height"),
            ],
        )

    @classmethod
    def execute(cls, aspect_ratio, megapixels, multiple, custom_ratio="4:3", batch_size=1, image=None):
        if image is not None:
            height, width = image.shape[1:3]
        else:
            ratio = custom_ratio if aspect_ratio == "Custom" else aspect_ratio.split(" ", 1)[0]
            try:
                width, height = map(float, ratio.split(":"))
            except ValueError:
                raise ValueError("Aspect ratio must use width:height, for example 4:3 or 9:16.") from None
        width, height = resolution(megapixels, multiple, width, height)
        latent = nodes.EmptyLatentImage().generate(width, height, batch_size)[0]
        return io.NodeOutput(latent, width, height, ui={"resolution": [f"{width} × {height} · {width * height / (1024 * 1024):.2f} MP"]})


class AspectRatioLatentExtension(ComfyExtension):
    async def get_node_list(self):
        return [AspectRatioEmptyLatent]


async def comfy_entrypoint():
    return AspectRatioLatentExtension()
