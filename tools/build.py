import subprocess
import json
from pathlib import Path
from datetime import datetime

from tools.validate import ProtocolValidator
from engine.core import CatarEngine
from tools.export import Exporter


class BuildSystem:
    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.protocol_dir = self.root / "src/protocol"
        self.scoring_file = self.protocol_dir / "scoring.json"
        self.samples_dir = self.root / "data/samples"
        self.reports_dir = self.root / "output/reports"

        self.engine = CatarEngine(str(self.protocol_dir), str(self.scoring_file))
        self.exporter = Exporter()

    # ---------------------------------------------------------
    # 1. Validation du protocole
    # ---------------------------------------------------------
    def validate_protocol(self):
        print("\n=== VALIDATION DU PROTOCOLE ===")
        validator = ProtocolValidator(protocol_dir=str(self.protocol_dir))
        validator.run()
        if validator.errors:
            print("❌ Build interrompu : protocole invalide.")
            return False
        print("✔️ Protocole valide.")
        return True

    # ---------------------------------------------------------
    # 2. Exécution des tests unitaires
    # ---------------------------------------------------------
    def run_tests(self):
        print("\n=== EXÉCUTION DES TESTS UNITAIRES ===")
        try:
            result = subprocess.run(
                ["pytest", "-q"],
                cwd=self.root,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.returncode != 0:
                print("❌ Build interrompu : tests échoués.")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution des tests : {e}")
            return False

        print("✔️ Tous les tests sont passés.")
        return True

    # ---------------------------------------------------------
    # 3. Génération du rapport automatique
    # ---------------------------------------------------------
    def generate_report(self):
        print("\n=== GÉNÉRATION DU RAPPORT ===")

        # Chargement des réponses d'exemple
        phase1 = self._load_json(self.samples_dir / "before.json")
        phase2 = self._load_json(self.samples_dir / "after.json")
        phase3 = self._load_json(self.samples_dir / "after.json")

        if not phase1 or not phase2 or not phase3:
            print("❌ Impossible de générer le rapport : fichiers samples manquants.")
            return None

        p1 = self.engine.evaluate_phase1(phase1)
        p2 = self.engine.evaluate_phase2(phase2)
        p3 = self.engine.evaluate_phase3(phase1, phase3)

        final = self.engine.aggregate_scores(p1, p2, p3)

        # Sauvegarde du rapport Markdown
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        filename = f"build_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        path = self.reports_dir / filename

        md = []
        md.append("# Rapport automatique CATAR\n")
        md.append(f"**Date :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append("---\n")
        md.append(f"Score global : **{final['score_global']} / {final['max_score']}**\n")
        md.append(f"Validation : **{'✔️ OK' if final['validated'] else '❌ NON'}**\n")
        md.append("\n---\n")
        md.append("## Données complètes\n")
        md.append("```json\n")
        md.append(json.dumps(final, indent=2, ensure_ascii=False))
        md.append("\n```\n")

        path.write_text("\n".join(md), encoding="utf-8")

        print(f"✔️ Rapport généré : {path}")
        return final

    # ---------------------------------------------------------
    # 4. Export automatique
    # ---------------------------------------------------------
    def export_results(self, results):
        print("\n=== EXPORT AUTOMATIQUE ===")
        paths = self.exporter.export_all(results)
        print("✔️ Exports générés :")
        for fmt, p in paths.items():
            print(f" - {fmt} : {p}")

    # ---------------------------------------------------------
    # Utilitaire JSON
    # ---------------------------------------------------------
    def _load_json(self, path: Path):
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur chargement JSON {path}: {e}")
            return None

    # ---------------------------------------------------------
    # Pipeline complet
    # ---------------------------------------------------------
    def run(self):
        print("\n====================================")
        print("        BUILD CATAR-SOFTWARE")
        print("====================================")

        if not self.validate_protocol():
            return

        if not self.run_tests():
            return

        results = self.generate_report()
        if results:
            self.export_results(results)

        print("\n====================================")
        print("✔️ BUILD TERMINÉ AVEC SUCCÈS")
        print("====================================")


if __name__ == "__main__":
    BuildSystem().run()

