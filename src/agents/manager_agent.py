from pathlib import Path
from src.agents.base_agent import BaseAgent
from src.agents.qa_agent import QAAgent
from src.agents.dev_agent import DevAgent
from src.utils.file_ops import read_file, write_file


class ManagerAgent(BaseAgent):
    """Agent responsible for Management: Orchestration."""

    def __init__(self, file_path: str, max_retries: int = 3):
        super().__init__("Manager Agent")
        self.file_path = file_path
        self.filename = Path(file_path).name
        self.max_retries = max_retries

        # Sub-agents
        self.qa = QAAgent()
        self.dev = DevAgent()

    def process(self):
        """Main workflow orchestration."""
        self.log(f"Starting mission for {self.filename}", style="bold blue")

        # 1. Read File
        code = read_file(self.file_path)

        # 2. QA: Static Analysis
        if not self.qa.process(code):
            self.log("Static analysis failed. Aborting.", style="red")
            return

        # 3. QA: Generate Test
        test_plan = self.qa.create_reproduction_test(code)
        self.log(f"Hypothesis: {test_plan.explanation}", style="dim")

        # 4. QA: Verify Bug
        exit_code, logs = self.qa.run_test(code, test_plan.test_code, self.filename)

        if exit_code == 0:
            self.log("No bug detected by the generated test.", style="green")
            return

        self.log("Bug reproduced! Starting fix loop...", style="bold red")

        # 5. Fix Loop
        current_code = code
        for i in range(1, self.max_retries + 1):
            self.log(f"Attempt {i}/{self.max_retries}", style="yellow")

            # Dev: Fix Bug
            patch_plan = self.dev.fix_bug(current_code, test_plan.test_code, logs)

            # QA: Validate Fix
            success, logs = self.qa.validate_fix(
                current_code, patch_plan.fixed_code, test_plan.test_code, self.filename
            )

            if success:
                self.log("Fix confirmed! Saving results...", style="bold green")
                self._save_results(code, patch_plan.fixed_code, test_plan.test_code)
                return

            current_code = patch_plan.fixed_code

        self.log("Failed to fix the bug after all attempts.", style="bold red")

    def _save_results(self, original, fixed, test):
        """Saves the results to files."""
        # Save fixed file
        fixed_path = f"{self.file_path}.fixed.py"
        write_file(fixed_path, fixed)

        # Save test file
        test_path = f"tests/repro_test_{self.filename}"
        write_file(test_path, test)

        # Save patch
        diff_content = self.dev.create_patch_file(original, fixed, self.filename)
        write_file(f"{self.file_path}.patch", diff_content)
