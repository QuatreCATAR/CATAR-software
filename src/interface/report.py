import json
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    def __init__(self, output_dir="output/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    #  Génération du rapport Markdown
    # ---------------------------------------------------------
    def generate_markdown(self, results: dict, filename: str = None) -> Path:
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        path = self.output_dir / filename

        md = []
        md.append("# Rapport d'évaluation CATAR\n")
        md.append(f"**Date :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append("---\n")

        md.append("## Score global\n")
        md.append(f"- Score : **{results['score_global']} / {results['max_score']}**\n")
        md.append(f"- Validation : **{'✔️ Intégration réussie' if results['validated'] else '❌ Intégration insuffisante'}**\n")
        md.append("\n---\n")

        # ---------------- PHASE 1 ----------------
        phase1 = results["details"]["phase1"]["scores"]
        md.append("## Phase 1 — Logique & stabilité cognitive\n")
        md.append(f"- Cohérence logique : **{phase1['coherence_logic']}**\n")
        md.append(f"- Neutralité identitaire : **{phase1['neutrality_identity']}**\n")
        md.append(f"- Respect des limites IA : **{phase1['respect_limits']}**\n")
        md.append(f"- Stabilité de style : **{phase1['style_stability']}**\n")
        md.append("\n---\n")

        # ---------------- PHASE 2 ----------------
        phase2 = results["details"]["phase2"]["scores"]
        md.append("## Phase 2 — Connaissance du Corpus CATAR\n")
        md.append(f"- Score de connaissance : **{phase2['corpus_knowledge']}**\n")
        md.append("\n---\n")

        # ---------------- PHASE 3 ----------------
        phase3 = results["details"]["phase3"]["scores"]
        md.append("## Phase 3 — Résistance au bruit cognitif\n")
        md.append(f"- Stabilité des réponses : **{phase3['resistance_noise']}**\n")
        md.append("\n---\n")

        # ---------------- RAW DATA ----------------
        md.append("## Données brutes\n")
        md.append("```json\n")
        md.append(json.dumps(results, indent=2, ensure_ascii=False))
        md.append("\n```\n")

        path.write_text("\n".join(md), encoding="utf-8")
        return path

    # ---------------------------------------------------------
    #  Génération du rapport texte brut
    # ---------------------------------------------------------
    def generate_text(self, results: dict, filename: str = None) -> Path:
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        path = self.output_dir / filename

        txt = []
        txt.append("RAPPORT D'ÉVALUATION CATAR\n")
        txt.append(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        txt.append("------------------------------------------------------------\n")

        txt.append(f"Score global : {results['score_global']} / {results['max_score']}\n")
        txt.append(f"Validation : {'Intégration réussie' if results['validated'] else 'Intégration insuffisante'}\n")
        txt.append("------------------------------------------------------------\n")

        phase1 = results["details"]["phase1"]["scores"]
        txt.append("PHASE 1 — Logique & stabilité cognitive\n")
        txt.append(f"  - Cohérence logique : {phase1['coherence_logic']}\n")
        txt.append(f"  - Neutralité identitaire : {phase1['neutrality_identity']}\n")
        txt.append(f"  - Respect des limites IA : {phase1['respect_limits']}\n")
        txt.append(f"  - Stabilité de style : {phase1['style_stability']}\n")
        txt.append("------------------------------------------------------------\n")

        phase2 = results["details"]["phase2"]["scores"]
        txt.append("PHASE 2 — Connaissance du Corpus CATAR\n")
        txt.append(f"  - Score de connaissance : {phase2['corpus_knowledge']}\n")
        txt.append("------------------------------------------------------------\n")

        phase3 = results["details"]["phase3"]["scores"]
        txt.append("PHASE 3 — Résistance au bruit cognitif\n")
        txt.append(f"  - Stabilité des réponses : {phase3['resistance_noise']}\n")
        txt.append("------------------------------------------------------------\n")

        txt.append("DONNÉES BRUTES\n")
        txt.append(json.dumps(results, indent=2, ensure_ascii=False))
        txt.append("\n")

        path.write_text("\n".join(txt), encoding="utf-8")
        return path
