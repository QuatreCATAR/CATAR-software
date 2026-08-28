import re
import sys
from pathlib import Path
import subprocess


class VersionManager:
    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.pyproject = self.root / "pyproject.toml"

    # ---------------------------------------------------------
    # Lire la version actuelle dans pyproject.toml
    # ---------------------------------------------------------
    def get_current_version(self):
        content = self.pyproject.read_text(encoding="utf-8")
        match = re.search(r'version\s*=\s*"(\d+\.\d+\.\d+)"', content)
        if not match:
            raise ValueError("Version introuvable dans pyproject.toml")
        return match.group(1)

    # ---------------------------------------------------------
    # Incrémenter la version
    # ---------------------------------------------------------
    def bump(self, current, mode):
        major, minor, patch = map(int, current.split("."))

        if mode == "patch":
            patch += 1
        elif mode == "minor":
            minor += 1
            patch = 0
        elif mode == "major":
            major += 1
            minor = 0
            patch = 0
        else:
            raise ValueError("Mode invalide : choisir major, minor ou patch")

        return f"{major}.{minor}.{patch}"

    # ---------------------------------------------------------
    # Mettre à jour pyproject.toml
    # ---------------------------------------------------------
    def update_pyproject(self, new_version):
        content = self.pyproject.read_text(encoding="utf-8")
        updated = re.sub(
            r'version\s*=\s*"\d+\.\d+\.\d+"',
            f'version = "{new_version}"',
            content
        )
        self.pyproject.write_text(updated, encoding="utf-8")
        print(f"✔ Version mise à jour dans pyproject.toml → {new_version}")

    # ---------------------------------------------------------
    # Créer un tag Git
    # ---------------------------------------------------------
    def create_tag(self, version):
        print("▶ Création du tag Git...")
        subprocess.run(["git", "tag", f"v{version}"], cwd=self.root, check=True)
        subprocess.run(["git", "push", "origin", f"v{version}"], cwd=self.root, check=True)
        print(f"✔ Tag v{version} créé et poussé.")

    # ---------------------------------------------------------
    # Pipeline complet
    # ---------------------------------------------------------
    def run(self, mode):
        print("\n====================================")
        print(f"   VERSIONING CATAR-SOFTWARE ({mode})")
        print("====================================")

        current = self.get_current_version()
        print(f"Version actuelle : {current}")

        new_version = self.bump(current, mode)
        print(f"Nouvelle version : {new_version}")

        self.update_pyproject(new_version)
        self.create_tag(new_version)

        print("\n====================================")
        print("✔ VERSIONING TERMINÉ")
        print("====================================")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python tools/version.py [major|minor|patch]")
        sys.exit(1)

    mode = sys.argv[1]
    VersionManager().run(mode)
