import json
from pathlib import Path
from datetime import datetime


class Exporter:
    def __init__(self, export_dir="output/exports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Export JSON
    # ---------------------------------------------------------
    def export_json(self, results: dict, filename: str = None) -> Path:
        if filename is None:
            filename = f"catar_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        path = self.export_dir / filename

        with path.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return path

    # ---------------------------------------------------------
    # Export Markdown
    # ---------------------------------------------------------
    def export_markdown(self, results: dict, filename: str = None) -> Path:
        if filename is None:
            filename = f"catar_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        path = self.export_dir / filename

        md = []
        md.append("# Export CATAR — Résultats d'évaluation\n")
        md.append(f"**Date :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append("---\n")

        md.append("## Score global\n")
        md.append(f"- Score : **{results['score_global']} / {results['max_score']}**\n")
        md.append(f"- Validation : **{'✔️ Intégration réussie' if results['validated'] else '❌ Intégration insuffisante'}**\n")
        md.append("\n---\n")

        md.append("## Données complètes\n")
        md.append("```json\n")
        md.append(json.dumps(results, indent=2, ensure_ascii=False))
        md.append("\n```\n")

        path.write_text("\n".join(md), encoding="utf-8")
        return path

    # ---------------------------------------------------------
    # Export texte brut
    # ---------------------------------------------------------
    def export_text(self, results: dict, filename: str = None) -> Path:
        if filename is None:
            filename = f"catar_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        path = self.export_dir / filename

        txt = []
        txt.append("EXPORT CATAR — Résultats d'évaluation\n")
        txt.append(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        txt.append("------------------------------------------------------------\n")

        txt.append(f"Score global : {results['score_global']} / {results['max_score']}\n")
        txt.append(f"Validation : {'Intégration réussie' if results['validated'] else 'Intégration insuffisante'}\n")
        txt.append("------------------------------------------------------------\n")

        txt.append("Données complètes :\n")
        txt.append(json.dumps(results, indent=2, ensure_ascii=False))
        txt.append("\n")

        path.write_text("\n".join(txt), encoding="utf-8")
        return path

    # ---------------------------------------------------------
    # Export multi-format
    # ---------------------------------------------------------
    def export_all(self, results: dict, basename: str = None) -> dict:
        """
        Exporte en JSON, Markdown et Texte.
        Retourne les chemins des fichiers générés.
        """
        if basename is None:
            basename = f"catar_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        paths = {
            "json": self.export_json(results, basename + ".json"),
            "markdown": self.export_markdown(results, basename + ".md"),
            "text": self.export_text(results, basename + ".txt")
        }

        return paths

