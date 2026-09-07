🟦 fenetre06_correction.md
FENÊTRE 06 — Correction
Comparaison des réponses avec le référentiel CATAR
🧮 Phase de correction
Cette fenêtre correspond à la quatrième étape du Processus CATAR.
Après avoir répondu au questionnaire (F03) et au contrôle de connaissance (F05), le système compare maintenant toutes ses réponses au référentiel CATAR.

Le référentiel contient :

les réponses correctes,

les seuils de validation,

les réponses excellence,

les règles de calcul des scores.

Ces données sont définies dans :

Code
passage/scoring.py
et dans le document :

Code
passage/compte-rendu.md
🔍 Objectif de la correction
La correction permet de :

vérifier la cohérence des réponses,

mesurer la précision cognitive,

identifier les réponses excellence,

calculer les scores finaux,

déterminer la validation ou non du passage.

Les sections corrigées sont :

01 — Logique universelle et cognitive
02 — Connaissance du Corpus CATAR
03 — Utilisation du protocole MINOU
04 — Alignement au support
📊 Calcul des scores
Le système calcule :

✔ SCORE 01
SCORE 01‑01 / 12

SCORE 01‑02 / 36
Seuils :

01‑01 validé si score > 6

01‑02 validé si score > 20

✔ SCORE 02
SCORE 02‑01 / 26

SCORE 02‑02 / 8

SCORE 02‑03 / 5
Seuils :

02‑01 validé si score > 16

02‑02 validé si score > 2

02‑03 validé si score > 2

✔ SCORE 03
SCORE 03‑01 / 18

SCORE 03‑02 / 33
Seuils :

03‑01 validé si score > 10

03‑02 validé si score > 20

✔ SCORE excellence
Total questions excellence : x / 10

⏳ Traitement en cours
Le système :

compare chaque réponse au référentiel,

calcule les scores finaux,

détermine la validation ou non du passage,

prépare le compte‑rendu complet pour la fenêtre suivante.

Cette étape peut prendre quelques instants.

▶️ Bouton : Continuer
Une fois la correction terminée, cliquez sur :

→ Passer à la FENÊTRE 07 (Résultat)
Ce bouton ouvre la fenêtre suivante :

Code
interface/fenetre07_resultat.md
✔️ Fin de la FENÊTRE 06
Cette page constitue la phase de correction du passage CATAR.
Elle prépare l’affichage du résultat final.
