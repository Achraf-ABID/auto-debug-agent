import logging
from rich.console import Console
from rich.logging import RichHandler

console = Console(width=120, force_terminal=True)


def setup_logger(name="bug_hunter"):
    """Configure un logger riche et coloré."""
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=console, markup=True)],
    )
    return logging.getLogger(name)


logger = setup_logger()
