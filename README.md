# XDownload

CLI para baixar videos de redes sociais usando yt-dlp.

## Plataformas Suportadas

- Twitter/X

Quer adicionar mais? Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Requisitos

- Python 3.10+
- yt-dlp
- ffmpeg

## Instalacao

```bash
git clone git@github.com:RafaTheMonk/BaixadorVideos.git
cd BaixadorVideos
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

Baixar video (detecta plataforma automaticamente):
```bash
python xdownload.py https://x.com/usuario/status/123456789
```

Ver formatos disponiveis:
```bash
python xdownload.py --formatos https://x.com/usuario/status/123456789
```

Listar plataformas suportadas:
```bash
python xdownload.py --plataformas
```

Os videos sao salvos em `~/downloads_videos/`.

## Estrutura

```
BaixadorVideos/
├── downloaders/
│   ├── __init__.py    # Registro de downloaders
│   ├── base.py        # Classe base
│   └── twitter.py     # Twitter/X
├── xdownload.py       # CLI
├── requirements.txt
├── CONTRIBUTING.md    # Guia para contribuir
└── README.md
```

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para instrucoes de como adicionar suporte a novas plataformas.

## Licenca

MIT
