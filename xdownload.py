#!/usr/bin/env python3
"""
X/Twitter Video Downloader
==========================
Script para baixar vídeos do X (antigo Twitter) usando yt-dlp.

Autor: Seu Nome
Uso: python x_video_downloader.py <url_do_video>

Como funciona:
1. O yt-dlp faz uma requisição para a API do Twitter/X
2. Extrai os metadados do tweet (título, formatos disponíveis)
3. Baixa o stream de vídeo na melhor qualidade disponível
4. Se necessário, usa ffmpeg para mesclar áudio e vídeo

Tecnologias usadas:
- yt-dlp: Fork do youtube-dl, mais atualizado e com melhor suporte
- ffmpeg: Para processamento e merge de streams de mídia
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime

# yt-dlp pode ser usado como biblioteca Python
import yt_dlp


def extrair_tweet_id(url: str) -> str | None:
    """
    Extrai o ID do tweet da URL.
    
    O Twitter/X usa URLs no formato:
    - https://twitter.com/usuario/status/1234567890
    - https://x.com/usuario/status/1234567890
    - https://x.com/i/status/1234567890 (formato curto)
    
    O ID é sempre a última sequência numérica na URL.
    """
    # Regex para capturar o ID do status (sequência de dígitos após /status/)
    pattern = r'/status/(\d+)'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    return None


def validar_url(url: str) -> bool:
    """
    Valida se a URL é do Twitter/X.
    
    Aceita tanto twitter.com quanto x.com (após o rebranding).
    """
    patterns = [
        r'https?://(www\.)?(twitter|x)\.com/.+/status/\d+',
        r'https?://(www\.)?(twitter|x)\.com/i/status/\d+',
    ]
    
    return any(re.match(pattern, url) for pattern in patterns)


def criar_diretorio_downloads() -> Path:
    """
    Cria um diretório para os downloads se não existir.
    Retorna o caminho do diretório.
    """
    download_dir = Path.home() / "downloads_x"
    download_dir.mkdir(exist_ok=True)
    return download_dir


def hook_progresso(d: dict) -> None:
    """
    Callback para mostrar o progresso do download.
    
    O yt-dlp chama essa função durante o download com um dicionário
    contendo informações sobre o status:
    - 'status': 'downloading', 'finished', 'error'
    - 'downloaded_bytes': bytes baixados
    - 'total_bytes': tamanho total (quando conhecido)
    - '_percent_str': string formatada com a porcentagem
    """
    if d['status'] == 'downloading':
        # Mostra progresso na mesma linha
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        print(f"\rBaixando: {percent} @ {speed}", end='', flush=True)

    elif d['status'] == 'finished':
        print(f"\nDownload concluido! Processando...")

    elif d['status'] == 'error':
        print(f"\nErro no download")


def baixar_video(url: str, output_dir: Path | None = None) -> dict:
    """
    Baixa um vídeo do Twitter/X.
    
    Parâmetros:
    -----------
    url : str
        URL do tweet contendo o vídeo
    output_dir : Path, opcional
        Diretório de destino. Se None, usa ~/downloads_x
    
    Retorna:
    --------
    dict com informações do vídeo baixado:
        - 'success': bool
        - 'filepath': caminho do arquivo (se sucesso)
        - 'title': título do vídeo
        - 'error': mensagem de erro (se falha)
    
    Como o yt-dlp funciona internamente:
    ------------------------------------
    1. Faz requisição para obter o "guest token" do Twitter
    2. Usa a API GraphQL do Twitter para obter metadados do tweet
    3. Extrai as URLs dos diferentes formatos de vídeo disponíveis
    4. Baixa o formato de melhor qualidade
    5. Se o vídeo tem streams separados de áudio/vídeo, usa ffmpeg para mesclar
    """
    
    if output_dir is None:
        output_dir = criar_diretorio_downloads()
    
    # Valida a URL antes de tentar baixar
    if not validar_url(url):
        return {
            'success': False,
            'error': 'URL inválida. Use uma URL do Twitter/X no formato: https://x.com/usuario/status/ID'
        }
    
    tweet_id = extrair_tweet_id(url)
    
    # Configurações do yt-dlp
    # Documentação completa: https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp
    ydl_opts = {
        # Template do nome do arquivo de saída
        # %(title)s = título do tweet
        # %(id)s = ID do tweet
        # %(ext)s = extensão do arquivo
        'outtmpl': str(output_dir / '%(title).50s_%(id)s.%(ext)s'),
        
        # Formato: melhor qualidade de vídeo + melhor qualidade de áudio
        # O 'b' significa 'best' (melhor)
        # Alternativas: 'worst', 'bestvideo+bestaudio', 'bestvideo[height<=720]+bestaudio'
        'format': 'best',
        
        # Callback para progresso
        'progress_hooks': [hook_progresso],
        
        # Opções de merge (quando vídeo e áudio estão separados)
        'merge_output_format': 'mp4',
        
        # Não imprimir para stdout (usamos nosso próprio hook)
        'quiet': True,
        'no_warnings': True,
        
        # Tentar novamente em caso de erro de rede
        'retries': 3,
        
        # Timeout de conexão (segundos)
        'socket_timeout': 30,
        
        # Manter metadados do vídeo
        'writethumbnail': False,  # Mudar para True se quiser a thumbnail
        
        # Extrair informações sem baixar (útil para debug)
        # 'simulate': True,  # Descomente para testar sem baixar
    }
    
    resultado = {
        'success': False,
        'filepath': None,
        'title': None,
        'error': None,
        'tweet_id': tweet_id,
    }
    
    try:
        # YoutubeDL é a classe principal do yt-dlp
        # Usar como context manager garante cleanup adequado
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Iniciando download do tweet: {tweet_id}")
            print(f"Salvando em: {output_dir}")
            print("-" * 50)
            
            # extract_info faz o trabalho pesado:
            # 1. Identifica o extractor correto (neste caso, Twitter)
            # 2. Faz as requisições necessárias
            # 3. Baixa o vídeo se download=True
            info = ydl.extract_info(url, download=True)
            
            if info:
                # Constrói o caminho do arquivo baixado
                # prepare_filename usa o mesmo template que definimos em outtmpl
                filepath = ydl.prepare_filename(info)
                
                resultado['success'] = True
                resultado['filepath'] = filepath
                resultado['title'] = info.get('title', 'Sem título')
                resultado['duration'] = info.get('duration')
                resultado['uploader'] = info.get('uploader')
                resultado['view_count'] = info.get('view_count')
                resultado['like_count'] = info.get('like_count')
                
                print("-" * 50)
                print(f"Sucesso!")
                print(f"Arquivo: {filepath}")
                print(f"Autor: {resultado['uploader']}")
                if resultado['duration']:
                    print(f"Duracao: {resultado['duration']} segundos")
    
    except yt_dlp.utils.DownloadError as e:
        # Erros específicos de download (vídeo não encontrado, privado, etc)
        resultado['error'] = f"Erro de download: {str(e)}"
        print(f"\n{resultado['error']}")

    except yt_dlp.utils.ExtractorError as e:
        # Erros do extractor do Twitter (API mudou, rate limit, etc)
        resultado['error'] = f"Erro ao extrair informacoes: {str(e)}"
        print(f"\n{resultado['error']}")

    except Exception as e:
        # Outros erros inesperados
        resultado['error'] = f"Erro inesperado: {str(e)}"
        print(f"\n{resultado['error']}")
    
    return resultado


def listar_formatos(url: str) -> None:
    """
    Lista todos os formatos disponíveis para um vídeo.
    
    Útil para entender quais resoluções e codecs estão disponíveis.
    O Twitter geralmente oferece:
    - Vários perfis de qualidade (240p, 480p, 720p, 1080p)
    - Formato MP4 com codec H.264
    """
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    print(f"Analisando formatos disponiveis...")
    print("-" * 60)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if info and 'formats' in info:
                print(f"Titulo: {info.get('title', 'N/A')}")
                print(f"Uploader: {info.get('uploader', 'N/A')}")
                print("-" * 60)
                print(f"{'ID':<10} {'Extensão':<8} {'Resolução':<12} {'Nota':<20}")
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


def main():
    """
    Função principal - ponto de entrada do script.
    """
    
    print("=" * 60)
    print("X/Twitter Video Downloader")
    print("=" * 60)

    # Verifica argumentos da linha de comando
    if len(sys.argv) < 2:
        print("\nUso:")
        print(f"   python {sys.argv[0]} <url_do_tweet>")
        print(f"   python {sys.argv[0]} --formatos <url>  (para ver formatos)")
        print("\nExemplo:")
        print(f"   python {sys.argv[0]} https://x.com/usuario/status/123456789")
        return 1
    
    # Verifica se é para listar formatos
    if sys.argv[1] == '--formatos' and len(sys.argv) > 2:
        listar_formatos(sys.argv[2])
        return 0
    
    url = sys.argv[1]
    
    # Executa o download
    resultado = baixar_video(url)
    
    # Retorna código de saída apropriado
    return 0 if resultado['success'] else 1


# Este bloco só executa se o script for rodado diretamente
# (não quando importado como módulo)
if __name__ == "__main__":
    sys.exit(main())
