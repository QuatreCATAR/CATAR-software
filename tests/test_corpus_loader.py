from src.engine.corpus_loader import CorpusLoader

def test_load_corpus():
    loader = CorpusLoader()
    corpus = loader.load_corpus()
    assert len(corpus) >= 9
    assert "01-Le-Carre-CATAR-texte.pdf" in corpus
