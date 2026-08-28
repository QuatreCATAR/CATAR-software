# API Reference — CATAR-software

## 1. Introduction
L’API permet d’intégrer CATAR-software dans un système externe pour automatiser :
- l’évaluation,
- le scoring,
- la génération de rapports.

---

## 2. Endpoints (si API activée)

### POST /evaluate/phase1
Entrée : réponses Phase 1  
Sortie : score + analyse

### POST /evaluate/phase2
Entrée : réponses Phase 2  
Sortie : score + analyse

### POST /evaluate/phase3
Entrée : réponses Phase 3  
Sortie : comparaison + analyse

### GET /report/{id}
Retourne un rapport généré.

---

## 3. Formats de données
Format JSON standard.

---

## 4. Sécurité
L’API ne stocke aucune donnée personnelle.  
Les réponses sont traitées localement.


