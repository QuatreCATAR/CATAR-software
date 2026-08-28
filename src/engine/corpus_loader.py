import os
from pathlib import Path


class CorpusLoader:
    """
    Module de lecture du Corpus CATAR.
    Charge les fichiers .md et .pdf du dossier src/corpus/
    et les indexe dans une base interne.
    """

    def __init__(self, corpus_dir: str = "src/corpus"):
        self.corpus_dir = Path(corpus_dir)
        self.corpus_files = []
        self.corpus_data = {}

    def load_corpus(self):
        """Charge tous les fichiers du Corpus dans la mémoire."""
        if not self.corpus_dir.exists():
            raise FileNotFoundError(f"Dossier corpus introuvable : {self.corpus_dir}")

        for file in sorted(self.corpus_dir.iterdir()):
            if file.suffix.lower() in [".md", ".pdf"]:
                try:
                    content = self._read_file(file)
                    self.corpus_files.append(file.name)
                    self.corpus_data[file.name] = content
                except Exception as e:
                    print(f"⚠ Erreur lecture {file.name} : {e}")

        print(f"✔ Corpus chargé ({len(self.corpus_files)} fichiers)")
        return self.corpus_data

    def _read_file(self, file_path: Path) -> str:
        """Lecture simple du contenu texte (PDF ou Markdown)."""
        if file_path.suffix.lower() == ".md":
            return file_path.read_text(encoding="utf-8")

        elif file_path.suffix.lower() == ".pdf":
            try:
                import PyPDF2
                text = ""
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() or ""
                return text
            except Exception:
                return "[PDF non lisible — contenu binaire ignoré]"

        else:
            return "[Format non pris en charge]"

    def get_section(self, index: int) -> str:
        """Retourne le contenu du fichier n°index (1‑based)."""
        if index < 1 or index > len(self.corpus_files):
            raise IndexError("Index hors limites du Corpus.")
        filename = self.corpus_files[index - 1]
        return self.corpus_data.get(filename, "[Section vide]")


# Exemple d’utilisation directe
if __name__ == "__main__":
    loader = CorpusLoader()
    corpus = loader.load_corpus()
    print(f"Sections disponibles : {list(corpus.keys())}")
    print("\nExemple section 1 :\n", loader.get_section(1)[:500])
