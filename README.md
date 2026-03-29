# realesrgan-http-api

HTTP server that exposes a REST API for running Real-ESRGAN via the
`realesrgan-ncnn-vulkan` CLI.

## Features

- `POST /v0/api/upscale_image` endpoint for base64 image upscaling.
- Uses Real-ESRGAN CLI (`realesrgan-ncnn-vulkan`) under the hood.
- Model files are loaded from `models/`.

## Requirements

- Python 3.10+
- Real-ESRGAN NCNN Vulkan binary available in `PATH` as `realesrgan-ncnn-vulkan`
- Model files in `models/` (see below)

## Setup

1. Create and activate a virtualenv (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure the Real-ESRGAN CLI is installed and on your `PATH`:

```bash
realesrgan-ncnn-vulkan -h
```

4. Download and place models in `models/` (see below).

## Download Models

Model params must be present in the `models/` folder. The simplest approach
is to download the official release zip and copy the `models/` contents.

Release: `https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.2.5.0`

From the release zip:

1. Extract the archive.
2. Copy files from the extracted `models/` folder into this repo’s `models/`.

Included files typically look like:

- `realesrgan-x4plus.bin` / `.param`
- `realesrgan-x4plus-anime.bin` / `.param`
- `realesr-animevideov3-x2.bin` / `.param`
- `realesr-animevideov3-x3.bin` / `.param`
- `realesr-animevideov3-x4.bin` / `.param`

## Run

### Development (with reload)

```bash
python -m realesrgan_http_api
```

Default server: `http://localhost:8080`

### Installed script

```bash
pip install -e .
realesrgan-http-api
```

## API

### POST `/v0/api/upscale_image`

Request body (JSON):

```json
{
  "image": "<base64-encoded image>",
  "model": "realesrgan-x4plus",
  "scale": 4,
  "tile_size": 512
}
```

Fields:

- `image` (required): Base64-encoded input image bytes.
- `model` (required): Real-ESRGAN model name (must exist in `models/`).
- `scale` (required): Upscale factor, must be > 0.
- `tile_size` (optional): Tile size for the CLI. Use `0` to disable tiling.

Response body (JSON):

```json
{
  "upscaled_image": "<base64-encoded image>"
}
```

## Notes

- Temporary files are written under `temp_files/`.
- The server uses FastAPI + Uvicorn.
