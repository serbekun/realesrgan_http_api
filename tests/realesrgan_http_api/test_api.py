
import json
import sys
from typing import Any, Dict
import requests
import base64

DEFAULT_BASE_URL: str = "http://localhost:8080"
DEFAULT_MODEL: str = "realesrgan-x4plus"

def _post_json(endpoint: str,
    payload: Dict[str, Any],
    *,
    base_url: str = DEFAULT_BASE_URL
) -> Dict[str, Any]:
    """ POST *payload* as JSON to *endpoint* and return the decoded response. """
    url = f"{base_url}{endpoint}" # formatting URL

    # send request
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise RuntimeError(f"API request to {endpoint} failed: {exc}") from exc
    return response.json()


def upscale_image(
    model: str = DEFAULT_MODEL,
    scale: float = 4.0,
    tile_size: int = 512,
    base_url: str = DEFAULT_BASE_URL
) -> Dict[str, Any]:
    
    with open("test_image.png", "rb") as f:
        image_bytes = f.read()

    image_base64_bytes = base64.b64encode(image_bytes)
    image_base64_string = image_base64_bytes.decode("utf-8")
    
    payload = {
        "image": image_base64_string,
        "model": model,
        "scale": scale,
        "tile_size": tile_size,
    }
    return _post_json("/v0/api/upscale_image", payload, base_url=base_url)


def main():
    upscale_image_data: Dict[str, Any] = upscale_image()
    print(len(upscale_image_data["upscaled_image"]))
    print(upscale_image_data.keys())
    
    upscaled_image_base64: str = upscale_image_data["upscaled_image"]
    
    upscaled_image_bytes: bytes = base64.b64decode(upscaled_image_base64)

    with open("upscaled_image.png", "wb") as f:
        f.write(upscaled_image_bytes)

if __name__ == "__main__":
    main()
