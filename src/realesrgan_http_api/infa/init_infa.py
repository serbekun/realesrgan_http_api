import os
from pathlib import Path
from src.realesrgan_http_api.config.infra import *

def init_infrastructure() -> None:
    """ Initializes the required project infrastructure. """
    init_folders()


def init_folders() -> None:
    """ Creates the required directories if they do not exist. """
    directories: list[str] = required_directories

    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
