# IAAS TP1 - EPITA Google Cloud YouTube App

## Description

Ce projet est une application de traitement de données YouTube, utilisant FastAPI pour l'API et Celery pour la planification des tâches. Le projet comprend deux composants principaux : l'API qui récupère les données de YouTube et les tâches qui traitent ces données et les enregistrent dans une base de données PostgreSQL.

## Prérequis

Avant de pouvoir exécuter ce projet, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Docker
- Docker Compose

## Structure du projet

```
.
├── Dockerfile
├── Dockerfile.db
├── LICENSE
├── Makefile
├── README.md
├── auth.py
├── celery_app.py
├── celerybeat-schedule
├── credentials.json
├── docker-compose.yml
├── init_db.sh
├── main.py
├── postgres.py
├── requirements.txt
├── storage.py
├── test.ipynb
├── utils.py
└── youtube_api.py
```

## Instructions d'installation

### 1. Cloner le dépôt

```
git clone https://github.com/mkdir-Cocodrilo/iaas-tp1.git
cd iaas-tp1
```

### 2. Configurer les services

Pour configurer les services nécessaires, utilisez Docker et Docker Compose :

```
docker-compose -f docker-compose.env.yml up --build
```

### 3. Lancer le service

Pour lancer le service localement :

```
docker-compose -f docker-compose.env.yml up
```

### 4. Arrêter le service

Pour arrêter les services :

```
docker-compose -f docker-compose.env.yml down
```

## Utilisation

### 1. Accéder à l'API

Une fois les services démarrés, vous pouvez accéder à l'API via `http://localhost:8080`.

### 2. Exécuter des tâches

Les tâches de traitement de données sont planifiées via Celery. Les tâches peuvent être exécutées et planifiées automatiquement selon les besoins du projet.

### 3. Journaux

Pour vérifier les journaux des services, utilisez la commande suivante :

```
docker-compose -f docker-compose.env.yml logs
```

## Déploiement

Le projet peut être déployé sur Google Cloud Platform en utilisant des workflows GitHub Actions. Assurez-vous de configurer les secrets nécessaires pour l'authentification et les permissions dans votre dépôt GitHub.

### Variables d'environnement

Assurez-vous que les variables d'environnement nécessaires sont définies dans votre dépôt GitHub en tant que secrets :

- `DATABASE_URL`
- `WIF_PROVIDER`
- `WIF_SERVICE_ACCOUNT`

## Dépendances

- Python 3.9
- FastAPI
- SQLAlchemy
- Celery
- Docker
- Redis
- PostgreSQL

## Licence

MIT
