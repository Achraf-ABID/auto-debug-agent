import ast
from src.utils.logger import logger


class StaticAnalyzer:
    """Analyse statique du code pour vérifier la validité avant envoi à l'IA."""

    @staticmethod
    def check_syntax(code: str) -> bool:
        try:
            ast.parse(code)
            logger.info("Analyse statique (AST) : [green]OK[/green]")
            return True
        except SyntaxError as e:
            logger.error(f"Erreur de syntaxe détectée : {e}")
            return False
