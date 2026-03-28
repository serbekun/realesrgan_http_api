import asyncio
import subprocess
import os
from uuid import uuid4
import logging

from src.realesrgan_http_api.model_provider.model_provider import ModelProvider;

class CliModelProvider(ModelProvider):

    def __init__(self, cli_command_name: str,
                temp_files_folder: str):
        self.cli_command_name = cli_command_name
        self.temp_files_folder = temp_files_folder
        self.logger = logging.getLogger(__name__)


    async def upscale_image(self, image_bytes: bytes, scale: int = 4, model: str = "realesrgan-x4plus") -> bytes:
        """Make upscaled image use cli tool"""

        # save input data to file
        image_id: str = uuid4().hex

        input_path = f"{self.temp_files_folder}/input_image_{image_id}"
        output_path = f"{self.temp_files_folder}/out_put_image_{image_id}"
        
        self.logger.info(f"Starting upscaling: model={model}, scale={scale}, id={image_id}")

        try:
            # write input data
            with open(input_path, "wb") as f:
                f.write(image_bytes)
            
            # calling CLI
            await self._call_cli(input_path, output_path, model)
            
            self.logger.info(f"Upscaling completed successfully for id={image_id}")

            # read result
            return self._read_file(output_path)
        
        except Exception as e:
            self.logger.error(f"Upscaling failed for id={image_id}: {e}", exc_info=True)
            raise

        finally:
            # cleanup temp files
            for path in [input_path, output_path]:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception as e:
                        self.logger.warning(f"Warning: Failed to remove temp file {path}: {e}")


    async def _call_cli(
            self,
            input_path: str,
            output_path: str,
            model: str = "realesrgan-x4plus",
            scale: int = 4,
            tile_size: int = 512
        ):
            """Call Real-ESRGAN CLI tool"""
            
            loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
            
            cmd = [
                self.cli_command_name,
                "-i", input_path,
                "-o", output_path,
                "-n", model,
                "-s", str(scale),
                "-t", "4",
            ]

            if tile_size:
                cmd.extend(["--tile", str(tile_size)])

            self.logger.debug(f"Running CLI command: {' '.join(cmd)}")

            result = await loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=False
                )
            )

            if result.returncode != 0:
                        self.logger.error(
                            f"CLI failed with code {result.returncode}\n"
                            f"stdout: {result.stdout}\n"
                            f"stderr: {result.stderr}"
                        )
                        raise Exception(
                            f"Real-ESRGAN CLI error (code {result.returncode}):\n"
                            f"stderr: {result.stderr}\nstdout: {result.stdout}"
                        )

            if not os.path.exists(output_path):
                raise Exception(f"Output file not created: {output_path}")

            self.logger.debug(f"CLI completed successfully, output: {output_path}")

    def _read_file(self, filepath: str) -> bytes:
        with open(filepath, "rb") as f:
            return f.read()
