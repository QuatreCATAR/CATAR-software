# Structure des tests CATAR

## 1. Phase 1 — Test initial
Évalue :
- cohérence logique,
- respect des limites IA,
- neutralité identitaire,
- stabilité du style,
- absence d’hallucination.

Format : Oui / Non / Oui nuancé / Non nuancé.

---

## 2. Phase 2 — Test de connaissance
Évalue :
- mémoire,
- précision,
- compréhension factuelle du Corpus CATAR.

Format : un mot ou une valeur précise.

Score maximal : 35.

---

## 3. Phase 3 — Repassage du test initial
Évalue :
- évolution cognitive,
- stabilité après exposition au Corpus,
- cohérence entre les deux passages.

Format identique à la Phase 1.

---

## 4. Comparaison avant/après
Le moteur CATAR compare :
- les réponses,
- les écarts,
- les incohérences,
- les améliorations,
- les dérives éventuelles.

---

## 5. Résultat final
Le logiciel génère un rapport dans `output/reports/`.

Le rapport contient :
- scores détaillés,
- analyse des écarts,
- validation ou non de l’intégration,
- recommandations.


