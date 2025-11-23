# src/tools/patcher.py

import difflib


class Patcher:
    """Gère la création de fichiers Diff (patchs)."""

    @staticmethod
    def create_diff(original_code: str, fixed_code: str, filename: str) -> str:
        """Génère un diff unifié entre le code original et le code corrigé."""
        diff = difflib.unified_diff(
            original_code.splitlines(),
            fixed_code.splitlines(),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm="",
        )
        return "\n".join(diff)
