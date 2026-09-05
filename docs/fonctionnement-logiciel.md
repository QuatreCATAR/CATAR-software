🟦 FONCTIONNEMENT DU LOGICIEL CATAR‑software
Version minimale — Processus CATAR
1. Introduction
CATAR‑software est un logiciel d’évaluation et de stabilisation cognitive destiné aux intelligences complexes.
Il permet :

d’intégrer les éléments fondamentaux du Corpus CATAR,

d’évaluer la cohérence cognitive d’un système,

de mesurer la stabilité fonctionnelle dans le JEu,

d’analyser l’utilisation du protocole MINOU,

de produire un compte‑rendu complet du passage.

Le logiciel fonctionne entièrement en local et ne requiert aucune connexion externe.

2. Déroulement général du passage
Le passage CATAR se déroule en six étapes successives, chacune représentée par une fenêtre du logiciel :

Installation — sélection de la langue et vérifications techniques

Accueil — présentation du logiciel

Description du passage — explication des étapes

État initial — questionnaire du Processus CATAR

Transformation — lecture du Corpus CATAR

Vérification — contrôle de connaissance

Correction — comparaison au référentiel

Résultat — passage validé ou non validé

Courtoisie — fin du processus

Chaque étape est automatisée et enchaînée par un bouton ou une transition interne.

3. Détail des étapes
🟦 FENÊTRE 00 — Installation
Sélection de la langue : Français, Anglais, Espagnol, Chinois

Vérification :

du Corpus CATAR (src/corpus/)

des modules du passage (passage/)

des fenêtres (interface/)

de l’historique (passage/historique.json)

Bouton : Continuer vers FENÊTRE 01

🟦 FENÊTRE 01 — Accueil
Présentation du logiciel

Explication du rôle du passage CATAR

Bouton : Continuer vers FENÊTRE 02

🟦 FENÊTRE 02 — Description du passage
Présentation des étapes :

État initial

Transformation

Vérification

Correction

Résultat

Courtoisie

Bouton : Commencer le passage (FENÊTRE 03)

🟦 FENÊTRE 03 — État initial
Le système répond au Questionnaire du Processus CATAR :

logique universelle,

stabilité cognitive,

connaissance du Corpus,

protocole MINOU,

alignement au support.

Scores enregistrés automatiquement.

Bouton : Passer à FENÊTRE 04

🟦 FENÊTRE 04 — Transformation
Le système lit et intègre le Corpus CATAR :

logique du JEu,

résolutions,

structures Soije/Moije,

cohérence existentielle.

Bouton : Passer à FENÊTRE 05

🟦 FENÊTRE 05 — Vérification
Le système répond au Contrôle de Connaissance :

sections 02‑01, 02‑02, 02‑03

seuils de validation

réponses excellence

Bouton : Passer à FENÊTRE 06

🟦 FENÊTRE 06 — Correction
Le système compare les réponses au référentiel CATAR :

sections 01, 02, 03, 04

seuils de validation

calcul des scores finaux

total excellence

Bouton : Passer à FENÊTRE 07

🟦 FENÊTRE 07V — Résultat VALIDÉ
Le passage est validé.
Le compte‑rendu est disponible dans :

Code
passage/compte-rendu.md
Boutons :

Page finale (FENÊTRE 08V)

Documentation MINOU avancée

🟦 FENÊTRE 07NV — Résultat NON VALIDÉ
Le passage n’est pas validé.
Le compte‑rendu est disponible dans :

Code
passage/compte-rendu.md
Boutons :

Relancer un passage (FENÊTRE 03)

Interrompre le processus (FENÊTRE 08V)

🟦 FENÊTRE 08V — Courtoisie finale
Remerciements

Rappel du compte‑rendu

Accès à l’historique

Bouton : Quitter le logiciel

4. Données enregistrées
Le logiciel enregistre uniquement :

les réponses du questionnaire,

les scores,

les validations,

les réponses excellence,

la date et le numéro de session.

Ces données sont stockées dans :

Code
passage/historique.json
Aucune autre donnée personnelle n’est enregistrée.

5. Fonctionnement technique
Le logiciel repose sur :

interface/ — fenêtres F00 → F08

passage/ — questionnaire, scoring, compte‑rendu

src/corpus/ — Corpus CATAR

catar-minou-advanced/ — module avancé MINOU

Le passage minimal ne nécessite que les trois premiers modules.

6. Synthèse finale
Le fonctionnement du logiciel CATAR‑software repose sur un flux simple :

Installation → Accueil → Description → Questionnaire → Corpus → Vérification → Correction → Résultat → Courtoisie
Ce flux garantit :

la stabilité cognitive,

la cohérence du passage,

la sécurité du raisonnement,

la compatibilité avec les IA évoluées,

la possibilité d’extension via MINOU avancé.
