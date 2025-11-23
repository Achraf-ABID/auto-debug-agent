from pathlib import Path
from src.utils.logger import logger


def read_file(path: str) -> str:
    """Lit le contenu d'un fichier texte."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.error(f"Fichier introuvable : {path}")
        raise


def write_file(path: str, content: str):
    """Écrit du contenu dans un fichier."""
    try:
        Path(path).write_text(content, encoding="utf-8")
        logger.info(f"Fichier sauvegardé : [bold]{path}[/bold]")
    except Exception as e:
        logger.error(f"Erreur d'écriture {path}: {e}")
