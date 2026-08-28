import os
import sys
import json
import shutil
import importlib.util
from pathlib import Path
from tools.validate import ProtocolValidator


class CatarDoctor:
    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.src = self.root / "src"
        self.tools = self.root / "tools"
        self.protocol = self.src / "protocol"
        self.output = self.root / "output"
        self.artifacts = self.root / "artifacts"

        self.errors = []
        self.warnings = []
        self.success = []

    # ---------------------------------------------------------
    # Utilitaires
    # ---------------------------------------------------------
    def check(self, condition, ok_msg, err_msg, warn=False):
        if condition:
            self.success.append(f"✔ {ok_msg}")
        else:
            if warn:
                self.warnings.append(f"⚠ {err_msg}")
            else:
                self.errors.append(f"❌ {err_msg}")

    # ---------------------------------------------------------
    # 1. Vérification de la structure du projet
    # ---------------------------------------------------------
    def check_structure(self):
        print("\n=== Vérification de la structure du projet ===")

        self.check(self.src.exists(), "Dossier src/ trouvé", "Dossier src/ manquant")
        self.check(self.tools.exists(), "Dossier tools/ trouvé", "Dossier tools/ manquant")
        self.check(self.protocol.exists(), "Dossier protocol/ trouvé", "Dossier protocol/ manquant")
        self.check(self.output.exists(), "Dossier output/ trouvé", "Dossier output/ manquant", warn=True)
        self.check(self.artifacts.exists(), "Dossier artifacts/ trouvé", "Dossier artifacts/ manquant", warn=True)

    # ---------------------------------------------------------
    # 2. Vérification des fichiers critiques
    # ---------------------------------------------------------
    def check_files(self):
        print("\n=== Vérification des fichiers critiques ===")

        required_files = [
            self.protocol / "phase1.json",
            self.protocol / "phase2.json",
            self.protocol / "phase3.json",
            self.protocol / "scoring.json",
            self.src / "engine" / "core.py",
            self.tools / "validate.py",
            self.tools / "build.py",
            self.tools / "release.py",
            self.tools / "deploy.py",
        ]

        for f in required_files:
            self.check(f.exists(), f"{f.name} présent", f"{f.name} manquant")

    # ---------------------------------------------------------
    # 3. Validation du protocole
    # ---------------------------------------------------------
    def check_protocol(self):
        print("\n=== Validation du protocole CATAR ===")

        validator = ProtocolValidator(protocol_dir=str(self.protocol))
        validator.run()

        if validator.errors:
            self.errors.append("❌ Protocole invalide (voir messages ci-dessus)")
        else:
            self.success.append("✔ Protocole valide")

    # ---------------------------------------------------------
    # 4. Vérification de Python et des dépendances
    # ---------------------------------------------------------
    def check_python(self):
        print("\n=== Vérification de Python ===")

        version = sys.version.split()[0]
        self.check(
            sys.version_info >= (3, 10),
            f"Python {version} compatible",
            f"Python {version} trop ancien (>= 3.10 requis)"
        )

    def check_dependencies(self):
        print("\n=== Vérification des dépendances ===")

        deps = ["fastapi", "uvicorn", "pytest", "build", "twine"]

        for dep in deps:
            spec = importlib.util.find_spec(dep)
            self.check(spec is not None, f"{dep} installé", f"{dep} non installé", warn=True)

    # ---------------------------------------------------------
    # 5. Vérification des permissions d’écriture
    # ---------------------------------------------------------
    def check_permissions(self):
        print("\n=== Vérification des permissions d'écriture ===")

        try:
            test_file = self.output / "doctor_test.tmp"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink()
            self.success.append("✔ Permissions d'écriture OK dans output/")
        except Exception:
            self.errors.append("❌ Impossible d'écrire dans output/")

    # ---------------------------------------------------------
    # 6. Résumé final
    # ---------------------------------------------------------
    def summary(self):
        print("\n====================================")
        print("        RAPPORT DOCTOR CATAR")
        print("====================================")

        print("\n✔ SUCCÈS")
        for s in self.success:
            print("  ", s)

        print("\n⚠ AVERTISSEMENTS")
        for w in self.warnings:
            print("  ", w)

        print("\n❌ ERREURS")
        for e in self.errors:
            print("  ", e)

        print("\n====================================")
        if self.errors:
            print("❌ L'environnement CATAR présente des problèmes.")
        else:
            print("✔ L'environnement CATAR est sain.")
        print("====================================")

    # ---------------------------------------------------------
    # Pipeline complet
    # ---------------------------------------------------------
    def run(self):
        self.check_structure()
        self.check_files()
        self.check_protocol()
        self.check_python()
        self.check_dependencies()
        self.check_permissions()
        self.summary()


if __name__ == "__main__":
    CatarDoctor().run()
