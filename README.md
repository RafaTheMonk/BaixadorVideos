# XDownload

Script simples para baixar videos do X (antigo Twitter) usando yt-dlp.

## Requisitos

- Python 3.10+
- yt-dlp
- ffmpeg (para processamento de video)

## Instalacao

```bash
git clone https://github.com/seu-usuario/xdownload.git
cd xdownload
pip install -r requirements.txt
```

### Instalar ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

## Uso

Baixar video:
```bash
python xdownload.py https://x.com/usuario/status/123456789
```

Ver formatos disponiveis:
```bash
python xdownload.py --formatos https://x.com/usuario/status/123456789
```

Os videos sao salvos em `~/downloads_x/`.

## Como funciona

1. yt-dlp faz requisicao para a API do Twitter/X
2. Extrai metadados do tweet (titulo, formatos disponiveis)
3. Baixa o stream de video na melhor qualidade
4. Se necessario, usa ffmpeg para mesclar audio e video

## Licenca

MIT
