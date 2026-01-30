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
```

### Linux

**Arch Linux / CachyOS:**
```bash
sudo pacman -S python-yt-dlp ffmpeg
```

**Ubuntu / Debian:**
```bash
sudo apt install python3 python3-pip ffmpeg
pip install yt-dlp
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip ffmpeg
pip install yt-dlp
```

### macOS

```bash
brew install python ffmpeg yt-dlp
```

### Windows

1. **Instalar Python:**
   - Baixe em https://python.org/downloads
   - Durante a instalacao, marque "Add Python to PATH"

2. **Instalar ffmpeg:**
   - Baixe em https://ffmpeg.org/download.html
   - Extraia e adicione a pasta `bin` ao PATH do sistema
   - Ou use winget: `winget install ffmpeg`

3. **Instalar yt-dlp:**
   ```cmd
   pip install yt-dlp
   ```

4. **Clonar o repositorio:**
   ```cmd
   git clone git@github.com:RafaTheMonk/BaixadorVideos.git
   cd BaixadorVideos
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

### Onde ficam os videos?

- **Linux/macOS:** `~/downloads_videos/`
- **Windows:** `C:\Users\SeuUsuario\downloads_videos\`

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
