import subprocess
from pathlib import Path
import sys


class DeployTool:
    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.dist_dir = self.root / "dist"

    # ---------------------------------------------------------
    # 1. Construction du package
    # ---------------------------------------------------------
    def build_package(self):
        print("\n=== Construction du package ===")

        # Nettoyage du dossier dist/
        if self.dist_dir.exists():
            for f in self.dist_dir.iterdir():
                f.unlink()
        else:
            self.dist_dir.mkdir()

        try:
            subprocess.run(
                [sys.executable, "-m", "build"],
                cwd=self.root,
                check=True
            )
            print("✔️ Package construit avec succès.")
        except subprocess.CalledProcessError as e:
            print("❌ Erreur lors de la construction du package :", e)
            sys.exit(1)

    # ---------------------------------------------------------
    # 2. Vérification des fichiers générés
    # ---------------------------------------------------------
    def check_dist(self):
        print("\n=== Vérification des fichiers dist/ ===")

        wheels = list(self.dist_dir.glob("*.whl"))
        sources = list(self.dist_dir.glob("*.tar.gz"))

        if not wheels or not sources:
            print("❌ Aucun fichier .whl ou .tar.gz trouvé dans dist/.")
            sys.exit(1)

        print("✔️ Fichiers trouvés :")
        for f in wheels + sources:
            print(" -", f)

    # ---------------------------------------------------------
    # 3. Publication sur PyPI ou TestPyPI
    # ---------------------------------------------------------
    def upload(self, repository="pypi"):
        print(f"\n=== Publication sur {repository} ===")

        try:
            subprocess.run(
                [
                    sys.executable, "-m", "twine", "upload",
                    "--repository", repository,
                    "dist/*"
                ],
                cwd=self.root,
                check=True
            )
            print(f"✔️ Publication réussie sur {repository}.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'upload vers {repository} :", e)
            sys.exit(1)

    # ---------------------------------------------------------
    # Pipeline complet
    # ---------------------------------------------------------
    def run(self, repository="pypi"):
        print("\n====================================")
        print("      DEPLOY CATAR-SOFTWARE")
        print("====================================")

        self.build_package()
        self.check_dist()
        self.upload(repository)

        print("\n====================================")
        print("✔️ DEPLOY TERMINÉ AVEC SUCCÈS")
        print("====================================")


if __name__ == "__main__":
    repo = "pypi"

    # Usage :
    # python tools/deploy.py testpypi
    # python tools/deploy.py pypi
    if len(sys.argv) > 1:
        repo = sys.argv[1]

    DeployTool().run(repository=repo)
