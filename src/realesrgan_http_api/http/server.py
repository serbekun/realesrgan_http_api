from typing import Any, Union, Tuple, Dict
from fastapi import FastAPI, Request
import logging
import base64
from src.realesrgan_http_api.config.infra import InfraConfig

from src.realesrgan_http_api.model_provider.model_provider import ModelProvider
from src.realesrgan_http_api.model_provider.cli.cli_model_provider import CliModelProvider


svr: FastAPI = FastAPI(title="src/realesrgan_http_api")
logger: logging.Logger = logging.getLogger(__name__)

model_provider: ModelProvider = CliModelProvider("realesrgan-ncnn-vulkan", InfraConfig.TEMP_FILES)


async def validate_v0_api_upscale_image_request_body(
    data: Dict[str, Any]
) -> Union[None, Tuple[Dict[str, str], int]]:
    """
    Validates the request body for the upscale_image endpoint.
    Returns None if everything is OK.
    Returns (error_dict, status_code) if there is an error.
    """
    if not data:
        logger.error("No data in request body")
        return {"details": "No data in request body"}, 400

    if "image" not in data or not data["image"]:
        logger.error("No image field in request json or image is empty")
        return {"details": "No image field in request json"}, 400

    if "scale" not in data:
        logger.error("No scale field in request json")
        return {"details": "No scale field in request json"}, 400

    if "model" not in data:
        logger.error("No model field in request json")
        return {"details": "No model field in request json"}, 400

    try:
        scale = float(data["scale"])
        if scale <= 0:
            return {"details": "scale must be greater than 0"}, 400
    except (ValueError, TypeError):
        return {"details": "scale must be a valid number"}, 400

    if "tile_size" in data:
        try:
            tile_size = int(data["tile_size"])
            if tile_size < 0:
                return {"details": "tile_size must be >= 0"}, 400
        except (ValueError, TypeError):
            return {"details": "tile_size must be an integer"}, 400

    # TODO add validate of base64 format

    return None  # Validation was successfully


@svr.post("/v0/api/upscale_image")
async def v0_api_upscale_image(request: Request):
    endpoint: str = "/v0/api/upscale_image"
    logger.info(f"Requested {endpoint}")

    try:
        data: Dict[str, Any] = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON body: {e}")
        return {"details": "Invalid or no JSON data in request body"}, 400

    validation_error = await validate_v0_api_upscale_image_request_body(data)
    if validation_error:
        return validation_error

    image_bytes: bytes = base64.b64decode(data["image"])

    upscaled_image_bytes: bytes = await model_provider.upscale_image(
        image_bytes,
        data["model"],
        data["scale"],
        data.get("tile_size", 512)
    )

    upscaled_image_base64: str = base64.b64encode(upscaled_image_bytes).decode("utf-8")

    return {"upscaled_image": upscaled_image_base64}
