# Contribuindo

Contribuicoes sao bem-vindas! Este guia explica como adicionar suporte a novas plataformas.

## Estrutura do Projeto

```
BaixadorVideos/
├── downloaders/
│   ├── __init__.py    # Registro de downloaders
│   ├── base.py        # Classe base abstrata
│   └── twitter.py     # Implementacao Twitter/X
├── xdownload.py       # CLI principal
├── requirements.txt
└── README.md
```

## Adicionando uma Nova Plataforma

### 1. Criar o arquivo do downloader

Crie um arquivo em `downloaders/` (ex: `youtube.py`):

```python
"""
Downloader para YouTube.
"""

import re
from .base import BaseDownloader


class YoutubeDownloader(BaseDownloader):
    """Downloader para videos do YouTube."""

    name = "youtube"
    supported_domains = ["youtube.com", "youtu.be"]

    def validate_url(self, url: str) -> bool:
        """Valida URL do YouTube."""
        patterns = [
            r'https?://(www\.)?youtube\.com/watch\?v=[\w-]+',
            r'https?://youtu\.be/[\w-]+',
        ]
        return any(re.match(pattern, url) for pattern in patterns)

    def extract_video_id(self, url: str) -> str | None:
        """Extrai ID do video."""
        patterns = [
            r'youtube\.com/watch\?v=([\w-]+)',
            r'youtu\.be/([\w-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_ydl_options(self) -> dict:
        """Opcoes especificas do YouTube (opcional)."""
        return {
            # Adicione opcoes especificas aqui
        }
```

### 2. Registrar o downloader

Edite `downloaders/__init__.py`:

```python
from .base import BaseDownloader
from .twitter import TwitterDownloader
from .youtube import YoutubeDownloader  # Adicionar import

DOWNLOADERS = {
    'twitter': TwitterDownloader,
    'x': TwitterDownloader,
    'youtube': YoutubeDownloader,  # Adicionar registro
    'yt': YoutubeDownloader,       # Alias opcional
}
```

### 3. Testar

```bash
python xdownload.py --plataformas
python xdownload.py https://youtube.com/watch?v=EXEMPLO
```

## Metodos da Classe Base

| Metodo | Obrigatorio | Descricao |
|--------|-------------|-----------|
| `validate_url(url)` | Sim | Valida se URL e valida |
| `extract_video_id(url)` | Sim | Extrai ID do video |
| `get_ydl_options()` | Nao | Opcoes especificas do yt-dlp |
| `supports_url(url)` | Nao | Verifica se suporta URL (usa `supported_domains`) |

## Atributos da Classe

| Atributo | Obrigatorio | Descricao |
|----------|-------------|-----------|
| `name` | Sim | Nome da plataforma |
| `supported_domains` | Sim | Lista de dominios suportados |

## Dicas

- Use regex para validacao e extracao de IDs
- Consulte a documentacao do yt-dlp para opcoes especificas
- Teste com diferentes formatos de URL da plataforma
- Mantenha o codigo simples e legivel

## Pull Request

1. Fork o repositorio
2. Crie uma branch: `git checkout -b feature/nova-plataforma`
3. Faca commit: `git commit -m "Add suporte para NovaPlatafroma"`
4. Push: `git push origin feature/nova-plataforma`
5. Abra um Pull Request

## Plataformas Sugeridas

- YouTube
- Instagram
- TikTok
- Facebook
- Vimeo
- Reddit
- Twitch (clips)
