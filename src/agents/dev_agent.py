from src.agents.base_agent import BaseAgent
from src.core.llm import LLMEngine
from src.tools.patcher import Patcher


class DevAgent(BaseAgent):
    """Agent responsible for Development: Fixing bugs."""

    def __init__(self):
        super().__init__("Dev Agent")
        self.llm = LLMEngine()
        self.patcher = Patcher()

    def process(self, code: str, test_code: str = "", error_logs: str = ""):
        """Main processing method - delegates to fix_bug."""
        return self.fix_bug(code, test_code, error_logs)

    def fix_bug(self, code: str, test_code: str, error_logs: str):
        """Analyzes logs and proposes a fix."""
        self.log("Analyzing logs and generating fix...", style="green")
        return self.llm.generate_patch(code, test_code, error_logs)

    def create_patch_file(self, original: str, fixed: str, filename: str) -> str:
        """Creates a unified diff patch."""
        return self.patcher.create_diff(original, fixed, filename)
