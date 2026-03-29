from abc import ABC, abstractmethod

class ModelProvider(ABC):
    
    @abstractmethod
    async def upscale_image(image_bytes: bytes, model: str = "realesrgan-x4plus", scale: int = 4, tile_size: int = 512) -> bytes:
        """ Method for upscale image """

        pass