"""Script de test avec plus de détails pour diagnostiquer le programme."""

import sys
import io

# Force utf-8 encoding for stdout/stderr on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from src.core.agent import BugHunterAgent
from src.utils.logger import logger

# Active le logging verbeux
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

try:
    print("=" * 80)
    print("TEST DU BUG HUNTER AGENT")
    print("=" * 80)

    agent = BugHunterAgent("examples/buggy_math.py", max_retries=3)
    agent.run()

    print("\n" + "=" * 80)
    print("Programme terminé")
    print("=" * 80)

except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
