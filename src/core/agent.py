from pathlib import Path
from rich.panel import Panel
from src.core.llm import LLMEngine
from src.core.sandbox import DockerSandbox
from src.tools.analyzer import StaticAnalyzer
from src.tools.patcher import Patcher
from src.utils.logger import logger, console
from src.utils.file_ops import read_file, write_file


class BugHunterAgent:
    def __init__(self, file_path: str, max_retries=3):
        self.file_path = file_path
        self.filename = Path(file_path).name
        self.max_retries = max_retries

        self.llm = LLMEngine()
        self.sandbox = DockerSandbox()
        self.analyzer = StaticAnalyzer()
        self.patcher = Patcher()

    def _update_test_with_fixed_code(
        self, test_code: str, original_code: str, fixed_code: str
    ) -> str:
        """Replace the original source code in the test with the fixed code."""
        # Simple replacement: find the original code block and replace it
        if original_code.strip() in test_code:
            return test_code.replace(original_code.strip(), fixed_code.strip())
        # Fallback: return test as-is if we can't find the code
        logger.warning("Could not find original code in test to replace")
        return test_code

    def run(self):
        console.print(
            Panel(
                f"Cible : {self.file_path}",
                title="🤖 Bug Hunter Agent",
                style="bold blue",
            )
        )

        # 1. Lecture et Analyse
        code = read_file(self.file_path)
        if not self.analyzer.check_syntax(code):
            return

        # 2. Génération du Test de Reproduction
        logger.info("Génération du test de reproduction...")
        test_plan = self.llm.generate_reproduction_test(code)
        console.print(f"[dim]Hypothèse : {test_plan.explanation}[/dim]")

        # 3. Validation du Bug (Le test DOIT échouer)
        exit_code, logs = self.sandbox.run_test(
            code, test_plan.test_code, self.filename
        )
        if exit_code == 0:
            console.print("[green]Aucun bug détecté par ce test.[/green]")
            return
        else:
            console.print("[red]Bug reproduit avec succès ![/red]")

        # 4. Boucle de Correction
        current_code = code
        for i in range(1, self.max_retries + 1):
            console.print(
                Panel(f"Tentative de correction {i}/{self.max_retries}", style="yellow")
            )

            patch_plan = self.llm.generate_patch(
                current_code, test_plan.test_code, logs
            )

            # DEBUG: Log the patch
            with open("debug_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n>>> Patch Proposed {i} <<<\n")
                f.write(patch_plan.explanation + "\n")
                f.write(patch_plan.fixed_code)
                f.write("\n>>>>>>>>>>>>>>>>>>>>>>\n")

            console.print(f"[dim]Logs Sandbox (Tentative {i}):[/dim]")
            console.print(Panel(logs, title="Sortie du Test", border_style="dim"))

            # DEBUG: Write logs to file
            with open("debug_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n--- Tentative {i} ---\n")
                f.write(logs)
                f.write("\n-------------------\n")

            # CRITICAL FIX: Update the test code with the fixed source code
            updated_test = self._update_test_with_fixed_code(
                test_plan.test_code, current_code, patch_plan.fixed_code
            )

            # Test de la correction with updated test
            exit_code, logs = self.sandbox.run_test(
                patch_plan.fixed_code, updated_test, self.filename
            )

            if exit_code == 0:
                console.print(
                    Panel("Succès : Le patch fonctionne !", style="bold green")
                )
                self._save_results(code, patch_plan.fixed_code, test_plan.test_code)
                return

            current_code = patch_plan.fixed_code  # On itère sur la nouvelle version

        console.print(
            "[bold red]Échec : Impossible de corriger le bug après les essais.[/bold red]"
        )

    def _save_results(self, original, fixed, test):
        # Sauvegarde fichier corrigé
        fixed_path = f"{self.file_path}.fixed.py"
        write_file(fixed_path, fixed)

        # Sauvegarde du test
        test_path = f"tests/repro_test_{self.filename}"
        write_file(test_path, test)

        # Sauvegarde du diff
        diff_content = self.patcher.create_diff(original, fixed, self.filename)
        write_file(f"{self.file_path}.patch", diff_content)
