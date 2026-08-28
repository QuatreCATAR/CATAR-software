# ============================================
# Makefile — CATAR-software (Développeur)
# ============================================

PYTHON=python

# Dossiers
SRC=src
TOOLS=tools
OUTPUT=output
ARTIFACTS=artifacts

# ============================================
# Commandes principales
# ============================================

# Validation du protocole
validate:
    @echo "▶ Validation du protocole..."
    $(PYTHON) $(TOOLS)/validate.py

# Tests unitaires
test:
    @echo "▶ Exécution des tests..."
    pytest -q

# Build complet (validation + tests + rapport + export)
build:
    @echo "▶ Build complet..."
    $(PYTHON) $(TOOLS)/build.py

# Lancer l'API FastAPI
api:
    @echo "▶ Lancement de l'API..."
    uvicorn src.interface.api:app --reload

# Lancer l'interface graphique
ui:
    @echo "▶ Lancement de l'interface graphique..."
    $(PYTHON) $(SRC)/interface/ui.py

# Installation locale du package
install:
    @echo "▶ Installation du package..."
    pip install .

# ============================================
# Release & Déploiement
# ============================================

# Release locale (tag + changelog + zip)
release:
    @if [ -z "$(v)" ]; then \
        echo "❌ Usage : make release v=1.2.0"; exit 1; \
    fi
    @echo "▶ Release locale version $(v)..."
    $(PYTHON) $(TOOLS)/release.py $(v)

# Déploiement PyPI (TestPyPI ou PyPI)
deploy:
    @if [ -z "$(repo)" ]; then \
        echo "❌ Usage : make deploy repo=testpypi"; exit 1; \
    fi
    @echo "▶ Déploiement sur $(repo)..."
    $(PYTHON) $(TOOLS)/deploy.py $(repo)

# ============================================
# Nettoyage
# ============================================

clean:
    @echo "🧹 Nettoyage des fichiers générés..."
    rm -rf $(OUTPUT)/*
    rm -rf $(ARTIFACTS)/*
    rm -rf dist/*
    rm -rf build/*
    rm -rf *.egg-info
    @echo "✔ Nettoyage terminé."

# ============================================
# Aide
# ============================================

help:
    @echo "Commandes disponibles :"
    @echo "  make validate        — valider le protocole"
    @echo "  make test            — exécuter les tests unitaires"
    @echo "  make build           — build complet (tests + rapport + export)"
    @echo "  make api             — lancer l'API FastAPI"
    @echo "  make ui              — lancer l'interface graphique"
    @echo "  make install         — installer le package local"
    @echo "  make release v=X.Y.Z — créer une release locale"
    @echo "  make deploy repo=pypi|testpypi — déployer sur PyPI"
    @echo "  make clean           — nettoyer les artefacts"
