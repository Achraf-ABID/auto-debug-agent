import docker
from src.utils.logger import logger


class DockerSandbox:
    """Gère l'exécution isolée via Docker SDK."""

    def __init__(self, image="python:3.10-slim"):
        try:
            self.client = docker.from_env()
            self.client.ping()
        except Exception:
            raise RuntimeError(
                "Docker n'est pas détecté. Veuillez installer et lancer Docker."
            )
        self.image = image
        self.container = None

    def ensure_image(self):
        try:
            self.client.images.get(self.image)
        except docker.errors.ImageNotFound:
            logger.info(f"Téléchargement de l'image {self.image}...")
            self.client.images.pull(self.image)

    def run_test(
        self, source_code: str, test_code: str, filename: str
    ) -> tuple[int, str]:
        self.ensure_image()

        import base64

        # Encodage Base64 pour éviter les problèmes de caractères spéciaux dans le shell
        b64_src = base64.b64encode(source_code.encode("utf-8")).decode("utf-8")
        b64_test = base64.b64encode(test_code.encode("utf-8")).decode("utf-8")
        test_filename = f"test_{filename}"

        # Commande : Crée dossiers -> Décode fichiers -> Installe pytest -> Lance test
        cmd = (
            f"/bin/sh -c '"
            f"mkdir -p /app && "
            f"echo {b64_src} | base64 -d > /app/{filename} && "
            f"echo {b64_test} | base64 -d > /app/{test_filename} && "
            f"pip install pytest -q > /dev/null && "
            f"pytest /app/{test_filename}'"
        )

        try:
            logger.info("Exécution Sandbox...")
            self.container = self.client.containers.run(
                self.image,
                command=cmd,
                working_dir="/app",
                detach=True,
                mem_limit="512m",  # Limite mémoire
            )

            self.container.wait(timeout=45)
            logs = self.container.logs().decode("utf-8")
            result = self.container.wait()

            return result["StatusCode"], logs

        except Exception as e:
            logger.error(f"Erreur Sandbox : {e}")
            return -1, str(e)
        finally:
            if self.container:
                try:
                    self.container.remove(force=True)
                except:
                    pass
