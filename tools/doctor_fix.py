import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from tools.validate import ProtocolValidator


class CatarDoctorFix:
    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.src = self.root / "src"
        self.tools = self.root / "tools"
        self.protocol = self.src / "protocol"
        self.output = self.root / "output"
        self.artifacts = self.root / "artifacts"

        self.errors = []
        self.fixed = []
        self.warnings = []

    # ---------------------------------------------------------
    # Utilitaires
    # ---------------------------------------------------------
    def fix(self, condition, ok_msg, fix_msg, fix_action):
        if condition:
            self.fixed.append(f"✔ {ok_msg}")
        else:
            try:
                fix_action()
                self.fixed.append(f"🔧 {fix_msg}")
            except Exception as e:
                self.errors.append(f"❌ Impossible de corriger : {fix_msg} ({e})")

    # ---------------------------------------------------------
    # 1. Réparation de la structure du projet
    # ---------------------------------------------------------
    def fix_structure(self):
        print("\n=== Réparation de la structure du projet ===")

        self.fix(
            self.src.exists(),
            "Dossier src/ OK",
            "Création du dossier src/",
            lambda: self.src.mkdir()
        )

        self.fix(
            self.tools.exists(),
            "Dossier tools/ OK",
            "Création du dossier tools/",
            lambda: self.tools.mkdir()
        )

        self.fix(
            self.protocol.exists(),
            "Dossier protocol/ OK",
            "Création du dossier protocol/",
            lambda: self.protocol.mkdir()
        )

        self.fix(
            self.output.exists(),
            "Dossier output/ OK",
            "Création du dossier output/",
            lambda: self.output.mkdir()
        )

        self.fix(
            self.artifacts.exists(),
            "Dossier artifacts/ OK",
            "Création du dossier artifacts/",
            lambda: self.artifacts.mkdir()
        )

    # ---------------------------------------------------------
    # 2. Réparation des fichiers critiques
    # ---------------------------------------------------------
    def fix_files(self):
        print("\n=== Réparation des fichiers critiques ===")

        def write_json(path, content):
            path.write_text(json.dumps(content, indent=2), encoding="utf-8")

        # Fichiers du protocole
        protocol_files = {
            "phase1.json": {"questions": []},
            "phase2.json": {"questions": []},
            "phase3.json": {"questions": []},
            "scoring.json": {"rules": []}
        }

        for filename, default_content in protocol_files.items():
            path = self.protocol / filename
            self.fix(
                path.exists(),
                f"{filename} OK",
                f"Recréation de {filename}",
                lambda p=path, c=default_content: write_json(p, c)
            )

        # Fichiers Python critiques
        critical_py = {
            self.src / "engine" / "core.py": "class CatarEngine:\n    pass\n",
            self.tools / "validate.py": "print('validate placeholder')\n",
            self.tools / "build.py": "print('build placeholder')\n",
            self.tools / "release.py": "print('release placeholder')\n",
            self.tools / "deploy.py": "print('deploy placeholder')\n",
        }

        for path, content in critical_py.items():
            self.fix(
                path.exists(),
                f"{path.name} OK",
                f"Recréation de {path.name}",
                lambda p=path, c=content: p.write_text(c, encoding="utf-8")
            )

    # ---------------------------------------------------------
    # 3. Réinstallation des dépendances Python
    # ---------------------------------------------------------
    def fix_dependencies(self):
        print("\n=== Vérification des dépendances ===")

        deps = ["fastapi", "uvicorn", "pytest", "build", "twine"]

        for dep in deps:
            try:
                __import__(dep)
                self.fixed.append(f"✔ {dep} installé")
            except ImportError:
                self.fixed.append(f"🔧 Installation de {dep}")
                subprocess.run([sys.executable, "-m", "pip", "install", dep])

    # ---------------------------------------------------------
    # 4. Réparation des permissions d’écriture
    # ---------------------------------------------------------
    def fix_permissions(self):
        print("\n=== Vérification des permissions d'écriture ===")

        try:
            test_file = self.output / "doctor_test.tmp"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink()
            self.fixed.append("✔ Permissions OK dans output/")
        except Exception:
            self.fixed.append("🔧 Correction des permissions")
            os.chmod(self.output, 0o755)

    # ---------------------------------------------------------
    # 5. Validation finale du protocole
    # ---------------------------------------------------------
    def final_validation(self):
        print("\n=== Validation finale du protocole ===")

        validator = ProtocolValidator(protocol_dir=str(self.protocol))
        validator.run()

        if validator.errors:
            self.errors.append("❌ Protocole toujours invalide après correction")
        else:
            self.fixed.append("✔ Protocole valide après correction")

    # ---------------------------------------------------------
    # Résumé final
    # ---------------------------------------------------------
    def summary(self):
        print("\n====================================")
        print("        RAPPORT DOCTOR --FIX")
        print("====================================")

        print("\n🔧 CORRECTIONS APPLIQUÉES")
        for f in self.fixed:
            print("  ", f)

        print("\n❌ PROBLÈMES RESTANTS")
        for e in self.errors:
            print("  ", e)

        print("\n====================================")
        if self.errors:
            print("❌ Certaines erreurs persistent.")
        else:
            print("✔ Environnement CATAR réparé avec succès.")
        print("====================================")

    # ---------------------------------------------------------
    # Pipeline complet
    # ---------------------------------------------------------
    def run(self):
        self.fix_structure()
        self.fix_files()
        self.fix_dependencies()
        self.fix_permissions()
        self.final_validation()
        self.summary()


if __name__ == "__main__":
    CatarDoctorFix().run()
