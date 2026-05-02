# API de Prédiction du Turnover Employés de la société TechNova Partners ESN

## Présentation du projet

Ce projet consiste à développer une API de prédiction du départ des employés (turnover) basée sur un modèle de Machine Learning développé à partir de données historiques de 1400 salariés fictifs de la société TecNova Partners.

L’API permet :

* une authentification sécurisée via JWT
* une prédiction du risque de départ d'un nouveau salarié de l'entreprise
* une explication de la contribution de chaque feature à la prédiction finale via la méthode  SHAP 
* la possibilité d'obtenir la courbe waterfall montrant le passage de l'espérance à la prédiction via un fichier encodé en base64
* un stockage des données d'entrée, des features et des données de sortie (prédiction, valeurs SHAP) en base PostgreSQL locale

Le projet s’inscrit dans une démarche MLOps complète :

* Développement d’un modèle ML
* Déploiement via API selon 3 méthodes (lancement en local avec uvicorn, lancement en local avec Docker et workflow ci-cd pour lancement de l'api conteneurisée sur un espace HuggingFace)
* Conteneurisation avec Docker
* Tests automatisés avec pytest
* Analyse de couverture de code

---

## Architecture du projet

app/ 
├── api/ # Routes API (auth, prédiction) 
├── core/ # Sécurité, config, dépendances 
├── db/ # Accès base de données 
├── ml/ # Pipeline ML 
├── schemas/ # Schémas Pydantic 
└── services/ # Logique métier 

data/ # Données locales + user.json 
models/ # Modèle ML + metadata 
scripts/ # Scripts DB & utilitaires 
tests/ # Tests pytest 
docker/ # Dockerfile

---

## Installation

### 1. Cloner le projet

```
git clone <repo>
cd projet
```

### 2. Installer les dépendances

```
pip install -r requirements.txt
```

ou avec uv :

```
uv sync
```

## Configuration de la base de données

La base de données PostgreSQL est créée et utilisée sur un serveur local.

Elle sera initialisée avec les trois scripts suivants:

```
- python scripts/db/create_db.py 
- python scripts/db/create_tables.py 
- python scripts/db/insert_employees.py
```

## Lancement de l'API

### Méthode 1 : local avec uvicorn

```
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API accessible en local avec swagger api sur:

```
http://<IP_DE_LA_MACHINE>:8000/docs  
```

### Méthode 2 : local avec Docker

Build:

```
docker build -f docker/Dockerfile -t ml-api .
```

Run:
```
docker run --network host \
-e POSTGRES_DB=<DB_NAME> \
-e POSTGRES_USER=<DB_USER> \
-e POSTGRES_PASSWORD=<DB_PASSWORD> \
-e POSTGRES_HOST=<DB_HOST> \
-e POSTGRES_PORT=<DB_PORT> \
ml-api
```

Les tests pytest doivent être exécutés avant le lancement du conteneur.

### Méthode 3 : Déploiement de l'API par workflow github actions sur un espace Hugging Face

L'API est lancée par deux workflows successifs github actions intégrant respectivement les fichiers ci-dessous:
```
.github/workflows/ci.yml
.github/workflows/ci-cd.yml
```
La méthode 3 repose sur un pipeline CI/CD en deux étapes :

-1. un premier workflow de CI exécute l’ensemble des tests automatisés (unitaires, API et pipeline ML avec pytest et coverage) à chaque push ou pull request sur la branche dev.

-2. puis un second workflow de CI/CD distinct prend le relais afin de builder l’image Docker située à la racine du projet et déployer automatiquement l’application sur Hugging Face Spaces.

Le résultat obtenu est:
-une API conteneurisée stateless et déployée sur Hugging Face
-pas d’accès à la base de données locale
-pas d’écriture en base
-prédiction, valeurs SHAP et waterfall en base64 uniquement

## Authentification

L'API utilise JWT.

Endpoint:

```
POST /auth/login
```

Exemple :
```
{ 
    "username": "admin", 
    "password": "Test123!" 
}
```

Réponse : 
```
{ 
    "access_token": "...", 
    "token_type": "bearer"
}
```

Utilisation:
```
Header :

Authorization: Bearer <token>
```

## Sécurité
Bonnes pratiques implémentées :
- Mots de passe hashés avec bcrypt
- Authentification JWT
- Pas de stockage de mots de passe en clair
- Utilisation de variables d’environnement (.env)
- Gestion des dépendances sécurisée

## Recommandations

- Ne jamais versionner .env
- Régénérer les tokens en production
- Utiliser une base distante sécurisée

## Prédiction

### Endpoint 

```
POST /predict
```

Entrée
```
{ 
        "employees": [...] 
}
``` 

Sortie
-probabilité
-features
-explications SHAP

## Explicabilité

### Endpoint 

```
POST /explain/waterfall
```

Retourne un graphique waterfall encodé en base 64.

Ce graphique peut être affiché sur une interface frontend à l'aide du script disponible sous:
```
scripts/ generation_waterfall.py
```

## Tests unitaires

### Cas méthodes 1 et 2 en local (uvicorm et Docker)

Lancer les tests unitaires à la racine du projet avec :
```
PYTHONPATH=. uv run pytest --cov=app --cov-report=html
```
Le rapport de couverture de code est ensuite disponible sous:
```
htmlcov/index.html
```

### Cas méthode 3 en déploiement (hugging face space)
un workflow spécifique est lancé avant déploiement avec le fichier ci-dessous:
```
.github/workflows/ci.yml
```

Le workflow github actions intégrant ce fichier exécute automatiquement les tests unitaires à chaque modification de code intégrat un push sur la branche dev. Ces tests ne comprennent pas le sous-ensemble dédié à la base de données locale et se limitent donc à:
-vérifier que les features sont construites comme attendu avant utilisation en inférence du modèle
-vérifier que l'API refuse correctement des données invalides 
-vérifier que la prédiction est valide avec une probabilité comprise entre 0 et 1 

Remarque: il reste à rendre dépendant le worklow ci-cd du résultat positif du premier workflow ci-dessus afin de déployer l'API en cas de succès des tests unitaires.

## Gestion des données d'entrée et de sortie

### Base de données locale
Stockage local dans une base de données PostgreSQL protégée par un mot de passe pour les méthodes 1 et 2.
La configuration initiale de cette base avec l'insertion des données historiques des 1400 salariés de l'entreprise est décrite plus
haut au paragraphe Configuration de la base de données.

Le diagramme uml de la base de données est disponible sous:
```
app/db/schema.png
app/db/schema.puml
```

La base comporte 4 tables: 
- une table employees comprenant les données historiques ainsi que celle des nouveaux salariés pour lesquels l'api de prédiction est utilisée
- une table de features intégrant toutes les features de l'ensemble X utilisé par le modèle en inférence pour prédire 
- une table prediction sauvegardant l'ensemble des résultats de prédictions (probabilité, espérance, valeurs shap)
- une table api\_logs historisant chaque interaction entre l'api et la base de données avec un timestamp (ecriture des données d'entrée et écriture des données de sortie de l'api de prédiction).

Remarque:
- les données historiques et anonymisées des 1470 salariés sont disponibles dans le fichier:
```
data/raw/employees.json
``` 

### limitations
- Base locale non accessible en cloud pour la méthode 3 (nécessité de créer une base de données sur un espace cloud)
- L'Authentification de la base a été simplifiée à un seul utilisateur
- Il reste encore à configurer une gestion multi-utilisateurs

## Améliorations possibles 
- créer une base de données cloud (AWS/GCP ou NéonDB) fonctionnant avec la méthode 3 devenant ainsi un mode 100% production
- configurer une authentification multi-utilisateurs pour la base de donées de cloud ainsi créée
- construire une interface utilisateur frontend permettant à l'utilisateur :
    - de s'authentifier pour accéder à l'api de prédiction
    - de rentrer les données d'un nouveau salarié
    - d'obtenir le résultat de prédiction avec le endpoint predict
    - d'afficher la courbe waterfall pour ce nouveau salarié

## Auteur
Projet réalisé dans le cadre de la formation Ai Engineer d'Openclassrooms 
Par: Viken Khatcherian

## Licence
MIT License





