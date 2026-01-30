#!/usr/bin/env python3
"""
XDownload - Video Downloader
============================

CLI para baixar videos de redes sociais usando yt-dlp.

Plataformas suportadas:
- Twitter/X

Uso:
    python xdownload.py <url>
    python xdownload.py --formatos <url>
    python xdownload.py --plataformas
"""

import sys
from pathlib import Path

from downloaders import detect_platform, get_downloader, DOWNLOADERS


def show_help():
    """Mostra ajuda de uso."""
    print("=" * 60)
    print("XDownload - Video Downloader")
    print("=" * 60)
    print("\nUso:")
    print(f"   python {sys.argv[0]} <url>")
    print(f"   python {sys.argv[0]} --formatos <url>")
    print(f"   python {sys.argv[0]} --plataformas")
    print("\nOpcoes:")
    print("   --formatos     Lista formatos disponiveis para o video")
    print("   --plataformas  Lista plataformas suportadas")
    print("\nExemplo:")
    print(f"   python {sys.argv[0]} https://x.com/usuario/status/123456789")


def show_platforms():
    """Lista plataformas suportadas."""
    print("Plataformas suportadas:")
    print("-" * 30)
    seen = set()
    for name, cls in DOWNLOADERS.items():
        if cls not in seen:
            seen.add(cls)
            domains = ", ".join(cls.supported_domains)
            print(f"  {cls.name}: {domains}")


def main():
    """Funcao principal."""
    if len(sys.argv) < 2:
        show_help()
        return 1

    arg = sys.argv[1]

    if arg == '--plataformas':
        show_platforms()
        return 0

    if arg == '--formatos':
        if len(sys.argv) < 3:
            print("Erro: URL necessaria")
            return 1
        url = sys.argv[2]
        platform = detect_platform(url)
        if not platform:
            print(f"Erro: URL nao reconhecida")
            return 1
        downloader_class = get_downloader(platform)
        downloader = downloader_class()
        downloader.list_formats(url)
        return 0

    url = arg
    platform = detect_platform(url)

    if not platform:
        print(f"Erro: URL nao reconhecida")
        print("Use --plataformas para ver plataformas suportadas")
        return 1

    print("=" * 60)
    print("XDownload - Video Downloader")
    print("=" * 60)

    downloader_class = get_downloader(platform)
    downloader = downloader_class()
    result = downloader.download(url)

    return 0 if result['success'] else 1


if __name__ == "__main__":
    sys.exit(main())
