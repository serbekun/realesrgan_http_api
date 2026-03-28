from abc import ABC, abstractmethod

class ModelProvider(ABC):
    
    @abstractmethod
    async def upscale_image(image_bytes: bytes, scale: int = 4, model: str = "realesrgan-x4plus") -> bytes:
        """ Method for upscale image """

        pass