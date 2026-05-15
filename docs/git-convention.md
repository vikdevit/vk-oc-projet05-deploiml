# Historique du projet 

## Branches utilisées 
- dev : développement (récupère par merge les fonctionnalités développées dans les branches ci-dessous)
- feature/api-fastapi : construction de l'api avec les endpoints (authentification, prediction, injection résultats dans base de données et waterfall) 
  feature/database : construction de la base de données locale (table des employés du dataset projet 4 + nouveaux employés testés avec le projet 5, table des features, table des prédictions et table de l'historique des interactions avec l'api)
- feature/hf-deployment : construction d'un fichier.yml de test (ci) et d'un fichier.yml de déploiement de l'api sur un espace personnalisé HuggingFace
- feature/init-structure : construction de l'arborescence du dossier du projet favorisant la modularité des scripts
- feature/tests : ensemble des scripts testants les différentes fonctionnalités et la cohérence du format des données fournies en inférence au modèle
-  main : branche qui sera utilisée lors de la création d'une base de données dans un espace cloud afin d'atteindre une portabilité de 100% du projet

## Tags
- 5b18a16 (tag: v0.1-structure-initiale) : marque la première version du projet, correspondant à l’initialisation de l’architecture du code
- bccff04 (tag: v1.0, origin/main) : marque une version stable du projet incluant un refactoring du pipeline ML et la mise en place du système d’inférence en production
 

## Convention de commits

---

### Format

<type>(<scope>): <description>

---

###  Types

#### feat
New feature

feat(api): add FastAPI predict endpoint
feat(ml): add FeatureBuilder

---

#### fix
Bug fixes

fix(ml): correct feature engineering mismatch

---

#### chore
Maintenance / setup / tooling

chore(repo): initialize project structure
chore(deps): update requirements

---

#### model
Machine Learning lifecycle (training, export, threshold)

model(training): export sklearn pipeline v1
model(threshold): optimize decision threshold

---

#### test
Tests

test(api): add /predict endpoint tests
test(ml): add FeatureBuilder unit tests

---

#### docs
Docs

docs(readme): update documentation et add project notes

---
