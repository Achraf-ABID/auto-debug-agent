import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
from src.agents.manager_agent import ManagerAgent

# Charger les variables d'environnement
load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Bug Hunter Agent - Multi-Agent System"
    )
    parser.add_argument("file", help="Chemin du fichier Python à analyser")
    parser.add_argument(
        "--retries", type=int, default=3, help="Nombre de tentatives de correction"
    )

    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        sys.exit(1)

    # Initialiser et lancer le Manager Agent
    agent = ManagerAgent(str(file_path), max_retries=args.retries)
    agent.process()


if __name__ == "__main__":
    main()
