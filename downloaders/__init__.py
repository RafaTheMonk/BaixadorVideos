from .base import BaseDownloader
from .twitter import TwitterDownloader

DOWNLOADERS = {
    'twitter': TwitterDownloader,
    'x': TwitterDownloader,
}


def get_downloader(platform: str) -> type[BaseDownloader]:
    """Retorna a classe do downloader para a plataforma especificada."""
    platform = platform.lower()
    if platform not in DOWNLOADERS:
        available = ', '.join(DOWNLOADERS.keys())
        raise ValueError(f"Plataforma '{platform}' nao suportada. Disponiveis: {available}")
    return DOWNLOADERS[platform]


def detect_platform(url: str) -> str | None:
    """Detecta a plataforma baseado na URL."""
    for name, downloader_class in DOWNLOADERS.items():
        if downloader_class.supports_url(url):
            return name
    return None
