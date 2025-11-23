from abc import ABC, abstractmethod
from rich.console import Console

console = Console()


class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(self, name: str):
        self.name = name
        self.console = console

    def log(self, message: str, style: str = "white"):
        """Log a message with the agent's name."""
        self.console.print(f"[{style}][{self.name}][/] {message}")

    @abstractmethod
    def process(self, *args, **kwargs):
        """Main processing method for the agent."""
        pass
