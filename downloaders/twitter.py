"""
Downloader para Twitter/X.
"""

import re
from .base import BaseDownloader


class TwitterDownloader(BaseDownloader):
    """Downloader para videos do Twitter/X."""

    name = "twitter"
    supported_domains = ["twitter.com", "x.com"]

    def validate_url(self, url: str) -> bool:
        """Valida URL do Twitter/X."""
        patterns = [
            r'https?://(www\.)?(twitter|x)\.com/.+/status/\d+',
            r'https?://(www\.)?(twitter|x)\.com/i/status/\d+',
        ]
        return any(re.match(pattern, url) for pattern in patterns)

    def extract_video_id(self, url: str) -> str | None:
        """Extrai ID do tweet."""
        pattern = r'/status/(\d+)'
        match = re.search(pattern, url)
        return match.group(1) if match else None
