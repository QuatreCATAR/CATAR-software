import subprocess
import sys
from pathlib import Path
from datetime import datetime


class LocalReleaseTool:
    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.artifacts = self.root / "artifacts"
        self.artifacts.mkdir(exist_ok=True)

    # ---------------------------------------------------------
    # 1. Génération du changelog local
    # ---------------------------------------------------------
    def generate_changelog(self, version: str) -> Path:
        print("\n=== Génération du changelog ===")

        changelog_path = self.artifacts / f"CHANGELOG_{version}.md"

        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:* %s", "--no-merges"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=True
            )
            content = f"# Changelog CATAR-software v{version}\n\n"
            content += result.stdout

            changelog_path.write_text(content, encoding="utf-8")
            print(f"✔️ Changelog généré : {changelog_path}")

        except Exception as e:
            print("❌ Erreur lors de la génération du changelog :", e)
            sys.exit(1)

        return changelog_path

    # ---------------------------------------------------------
    # 2. Création du tag Git
    # ---------------------------------------------------------
    def create_tag(self, version: str):
        print("\n=== Création du tag Git ===")

        try:
            subprocess.run(["git", "tag", f"v{version}"], cwd=self.root, check=True)
            subprocess.run(["git", "push", "origin", f"v{version}"], cwd=self.root, check=True)
            print(f"✔️ Tag v{version} créé et poussé.")
        except Exception as e:
            print("❌ Erreur lors de la création du tag :", e)
            sys.exit(1)

    # ---------------------------------------------------------
    # 3. Création du ZIP de release
    # ---------------------------------------------------------
    def create_zip(self, version: str) -> Path:
        print("\n=== Création du ZIP de release ===")

        zip_path = self.artifacts / f"CATAR-software-{version}.zip"

        try:
            subprocess.run(
                ["zip", "-r", str(zip_path), ".", "-x", "*.git*", "output/*", "artifacts/*"],
                cwd=self.root,
                check=True
            )
            print(f"✔️ Archive générée : {zip_path}")
        except Exception as e:
            print("❌ Erreur lors de la création du ZIP :", e)
            sys.exit(1)

        return zip_path

    # ---------------------------------------------------------
    # 4. Pipeline complet
    # ---------------------------------------------------------
    def run(self, version: str):
        print("\n====================================")
        print(f"   RELEASE LOCAL CATAR-SOFTWARE v{version}")
        print("====================================")

        changelog = self.generate_changelog(version)
        self.create_tag(version)
        zip_path = self.create_zip(version)

        print("\n====================================")
        print("✔️ RELEASE LOCALE TERMINÉE")
        print("Fichiers générés :")
        print(f" - Changelog : {changelog}")
        print(f" - Archive ZIP : {zip_path}")
        print("====================================")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python tools/release.py <version>")
        sys.exit(1)

    version = sys.argv[1]
    LocalReleaseTool().run(version)
