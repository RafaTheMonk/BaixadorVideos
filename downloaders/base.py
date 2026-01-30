"""
Classe base para downloaders de video.

Para adicionar suporte a uma nova plataforma, crie uma classe que herde de BaseDownloader
e implemente os metodos abstratos.

Exemplo:
    class YoutubeDownloader(BaseDownloader):
        name = "youtube"
        supported_domains = ["youtube.com", "youtu.be"]

        def validate_url(self, url: str) -> bool:
            # Implementar validacao
            pass

        def get_ydl_options(self) -> dict:
            # Retornar opcoes especificas do yt-dlp
            pass
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable
import re

import yt_dlp


class BaseDownloader(ABC):
    """Classe base abstrata para downloaders de video."""

    name: str = "base"
    supported_domains: list[str] = []

    def __init__(self, output_dir: Path | None = None):
        """
        Inicializa o downloader.

        Args:
            output_dir: Diretorio de saida. Se None, usa ~/downloads_videos
        """
        if output_dir is None:
            output_dir = Path.home() / "downloads_videos"
        output_dir.mkdir(exist_ok=True)
        self.output_dir = output_dir

    @classmethod
    def supports_url(cls, url: str) -> bool:
        """Verifica se o downloader suporta a URL."""
        for domain in cls.supported_domains:
            if domain in url.lower():
                return True
        return False

    @abstractmethod
    def validate_url(self, url: str) -> bool:
        """
        Valida se a URL e valida para esta plataforma.

        Args:
            url: URL do video

        Returns:
            True se a URL e valida
        """
        pass

    @abstractmethod
    def extract_video_id(self, url: str) -> str | None:
        """
        Extrai o ID do video da URL.

        Args:
            url: URL do video

        Returns:
            ID do video ou None se nao encontrado
        """
        pass

    def get_ydl_options(self) -> dict:
        """
        Retorna opcoes do yt-dlp especificas para esta plataforma.
        Sobrescreva para customizar.

        Returns:
            Dicionario com opcoes do yt-dlp
        """
        return {}

    def _create_progress_hook(self) -> Callable[[dict], None]:
        """Cria o hook de progresso padrao."""
        def hook(d: dict) -> None:
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                print(f"\rBaixando: {percent} @ {speed}", end='', flush=True)
            elif d['status'] == 'finished':
                print(f"\nDownload concluido! Processando...")
            elif d['status'] == 'error':
                print(f"\nErro no download")
        return hook

    def _get_base_options(self) -> dict:
        """Retorna opcoes base do yt-dlp."""
        return {
            'outtmpl': str(self.output_dir / '%(title).50s_%(id)s.%(ext)s'),
            'format': 'best',
            'progress_hooks': [self._create_progress_hook()],
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'retries': 3,
            'socket_timeout': 30,
        }

    def download(self, url: str) -> dict:
        """
        Baixa o video da URL.

        Args:
            url: URL do video

        Returns:
            Dicionario com resultado:
                - success: bool
                - filepath: caminho do arquivo (se sucesso)
                - title: titulo do video
                - error: mensagem de erro (se falha)
        """
        if not self.validate_url(url):
            return {
                'success': False,
                'error': f'URL invalida para {self.name}'
            }

        video_id = self.extract_video_id(url)
        options = {**self._get_base_options(), **self.get_ydl_options()}

        result = {
            'success': False,
            'filepath': None,
            'title': None,
            'error': None,
            'video_id': video_id,
            'platform': self.name,
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                print(f"Iniciando download: {video_id}")
                print(f"Salvando em: {self.output_dir}")
                print("-" * 50)

                info = ydl.extract_info(url, download=True)

                if info:
                    filepath = ydl.prepare_filename(info)
                    result['success'] = True
                    result['filepath'] = filepath
                    result['title'] = info.get('title', 'Sem titulo')
                    result['duration'] = info.get('duration')
                    result['uploader'] = info.get('uploader')

                    print("-" * 50)
                    print(f"Sucesso!")
                    print(f"Arquivo: {filepath}")
                    if result['uploader']:
                        print(f"Autor: {result['uploader']}")
                    if result['duration']:
                        print(f"Duracao: {result['duration']} segundos")

        except yt_dlp.utils.DownloadError as e:
            result['error'] = f"Erro de download: {str(e)}"
            print(f"\n{result['error']}")

        except yt_dlp.utils.ExtractorError as e:
            result['error'] = f"Erro ao extrair informacoes: {str(e)}"
            print(f"\n{result['error']}")

        except Exception as e:
            result['error'] = f"Erro inesperado: {str(e)}"
            print(f"\n{result['error']}")

        return result

    def list_formats(self, url: str) -> None:
        """Lista formatos disponiveis para o video."""
        options = {'quiet': True, 'no_warnings': True}

        print(f"Analisando formatos disponiveis...")
        print("-" * 60)

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)

                if info and 'formats' in info:
                    print(f"Titulo: {info.get('title', 'N/A')}")
                    print(f"Uploader: {info.get('uploader', 'N/A')}")
                    print("-" * 60)
                    print(f"{'ID':<10} {'Ext':<8} {'Resolucao':<12} {'Nota':<20}")
                    print("-" * 60)

                    for f in info['formats']:
                        format_id = f.get('format_id', 'N/A')
                        ext = f.get('ext', 'N/A')
                        resolution = f.get('resolution', 'N/A')
                        note = f.get('format_note', '')
                        print(f"{format_id:<10} {ext:<8} {resolution:<12} {note:<20}")
                else:
                    print("Nenhum formato encontrado.")

        except Exception as e:
            print(f"Erro ao listar formatos: {e}")
