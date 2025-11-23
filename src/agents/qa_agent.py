from src.agents.base_agent import BaseAgent
from src.core.llm import LLMEngine
from src.core.sandbox import DockerSandbox
from src.tools.analyzer import StaticAnalyzer


class QAAgent(BaseAgent):
    """Agent responsible for Quality Assurance: Analysis and Testing."""

    def __init__(self):
        super().__init__("QA Agent")
        self.llm = LLMEngine()
        self.sandbox = DockerSandbox()
        self.analyzer = StaticAnalyzer()

    def process(self, code: str) -> bool:
        """Basic syntax check."""
        self.log("Analyzing code syntax...", style="cyan")
        return self.analyzer.check_syntax(code)

    def create_reproduction_test(self, code: str):
        """Generates a test to reproduce the bug."""
        self.log("Generating reproduction test...", style="cyan")
        return self.llm.generate_reproduction_test(code)

    def run_test(self, code: str, test_code: str, filename: str) -> tuple[int, str]:
        """Runs the test in the sandbox."""
        self.log(f"Running tests for {filename}...", style="cyan")
        return self.sandbox.run_test(code, test_code, filename)

    def validate_fix(
        self, original_code: str, fixed_code: str, test_code: str, filename: str
    ) -> tuple[bool, str]:
        """Validates if the fix passes the test."""
        self.log("Validating fix...", style="cyan")

        # Update test with fixed code (using the logic we fixed earlier)
        updated_test = self._update_test_with_fixed_code(
            test_code, original_code, fixed_code
        )

        exit_code, logs = self.sandbox.run_test(fixed_code, updated_test, filename)

        success = exit_code == 0
        if success:
            self.log("Fix validated successfully! ✅", style="green")
        else:
            self.log("Fix failed validation. ❌", style="red")

        return success, logs

    def _update_test_with_fixed_code(
        self, test_code: str, original_code: str, fixed_code: str
    ) -> str:
        """Helper to replace code in test."""
        if original_code.strip() in test_code:
            return test_code.replace(original_code.strip(), fixed_code.strip())
        return test_code
