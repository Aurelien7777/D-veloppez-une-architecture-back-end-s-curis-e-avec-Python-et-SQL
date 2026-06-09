# Epic Events CRM

Application CRM interne développée en Python pour l'entreprise Epic Events.

Le projet permet aux collaborateurs de gérer les clients, les contrats et les événements de l'entreprise depuis une interface en ligne de commande.

## Fonctionnalités principales

* Authentification des collaborateurs
* Gestion des rôles :

  * management
  * commercial
  * support
* Gestion des clients
* Gestion des contrats
* Gestion des événements
* Attribution d'un membre support à un événement
* Filtrage des contrats non signés
* Filtrage des contrats non payés
* Filtrage des événements sans support
* Filtrage des événements assignés à un support
* Journalisation avec Sentry
* Validation des données utilisateur
* Protection contre les injections SQL via SQLAlchemy ORM
* Hash des mots de passe avec Argon2

## Technologies utilisées

* Python 3.12
* SQLAlchemy
* PyMySQL
* MySQL
* Poetry
* Argon2
* PyJWT
* Rich
* Sentry SDK
* Pytest
* Flake8
* Black

## Installation

Cloner le repository :

```bash
git clone https://github.com/Aurelien7777/D-veloppez-une-architecture-back-end-s-curis-e-avec-Python-et-SQL.git
cd projet_epic_events
```

Installer les dépendances avec Poetry :

```bash
poetry install
```

## Configuration des variables d'environnement

Créer un fichier `.env` à la racine du projet.

Exemple :

```env
DB_USER=epic_events_app
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_NAME=epic_events_crm

JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=8

SENTRY_DSN=your_sentry_dsn
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=0.0
```

Le fichier `.env` ne doit jamais être versionné.

Un fichier `.env.example` peut être ajouté au repository pour documenter les variables nécessaires sans exposer de données sensibles.

## Création de la base de données MySQL

Se connecter à MySQL :

```bash
mysql -u root -p
```

Créer la base de données :

```sql
CREATE DATABASE epic_events_crm
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Créer un utilisateur dédié :

```sql
CREATE USER 'epic_events_app'@'localhost' IDENTIFIED BY 'your_database_password';
GRANT ALL PRIVILEGES ON epic_events_crm.* TO 'epic_events_app'@'localhost';
FLUSH PRIVILEGES;
```

Quitter MySQL :

```sql
EXIT;
```

## Initialisation des tables

Depuis la racine du projet :

```bash
poetry run python -m epic_events.init_db
```

Cette commande crée les tables à partir des modèles SQLAlchemy.

## Création des rôles et du premier utilisateur management

Exécuter le script de seed :

```bash
poetry run python -m epic_events.scripts.seed
```

Ce script crée les rôles par défaut :

* management
* commercial
* support

Il permet aussi de créer le premier utilisateur management.

## Lancement de l'application

Depuis la racine du projet :

```bash
poetry run python -m epic_events.cli
```

## Commandes principales

### Lancer l'application

```bash
poetry run python -m epic_events.cli
```

### Lancer les tests

```bash
poetry run pytest
```

### Vérifier le style avec Flake8

```bash
poetry run flake8
```

### Formater le code avec Black

```bash
poetry run black .
```

## Structure du projet

```text
projet_epic_events/
├── epic_events/
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── contract_controller.py
│   │   ├── customer_controller.py
│   │   ├── event_controller.py
│   │   ├── permission_controller.py
│   │   ├── token_controller.py
│   │   └── user_controller.py
│   ├── menus/
│   │   ├── contract_menu.py
│   │   ├── customer_menu.py
│   │   ├── event_menu.py
│   │   └── user_menu.py
│   ├── models/
│   │   └── model.py
│   ├── repositories/
│   │   ├── base_repository.py
│   │   ├── contract_repository.py
│   │   ├── customer_repository.py
│   │   ├── event_repository.py
│   │   └── user_repository.py
│   ├── scripts/
│   │   └── seed.py
│   ├── views/
│   │   ├── auth_view.py
│   │   ├── console.py
│   │   ├── contract_view.py
│   │   ├── customer_view.py
│   │   ├── event_view.py
│   │   ├── input_helpers.py
│   │   ├── main_menu_view.py
│   │   └── user_view.py
│   ├── cli.py
│   ├── database.py
│   ├── exceptions.py
│   ├── init_db.py
│   ├── monitoring.py
│   └── validators.py
├── tests/
│   ├── functional/
│   └── unit/
├── .flake8
├── .gitignore
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Rôles et permissions

### Tous les collaborateurs

Tous les collaborateurs peuvent consulter les clients, les contrats et les événements.

### Management

Un utilisateur management peut :

* créer, modifier et supprimer des collaborateurs ;
* créer et modifier les contrats ;
* supprimer les clients, contrats et événements ;
* consulter les événements sans support ;
* assigner un membre support à un événement ;
* modifier le support assigné à un événement.

### Commercial

Un utilisateur commercial peut :

* créer des clients ;
* modifier les clients dont il est responsable ;
* modifier les contrats des clients dont il est responsable ;
* consulter les contrats non signés ;
* consulter les contrats non payés ;
* créer un événement pour un client dont le contrat est signé.

### Support

Un utilisateur support peut :

* consulter les événements qui lui sont assignés ;
* modifier les événements dont il est responsable.

## Sécurité

### Mots de passe

Les mots de passe ne sont jamais stockés en clair.

Ils sont hashés avec Argon2 avant d'être enregistrés en base de données.

### Authentification persistante

Après connexion, un token JWT est généré et stocké localement dans le dossier utilisateur.

Le token contient :

* l'identifiant utilisateur ;
* l'email ;
* le rôle ;
* la date de création ;
* la date d'expiration.

Si le token est invalide ou expiré, il est supprimé automatiquement.

### Protection contre les injections SQL

L'application utilise SQLAlchemy ORM.

Les requêtes sont construites avec `select()` et les filtres ORM, sans concaténation manuelle de chaînes SQL avec des entrées utilisateur.

### Principe du moindre privilège

Les permissions sont centralisées dans :

```text
epic_events/controllers/permission_controller.py
```

Chaque action sensible est contrôlée côté controller avant modification des données.

Exemples :

* seul le management peut créer un collaborateur ;
* seul le commercial responsable d'un client peut modifier ce client ;
* seul le commercial responsable d'un client peut créer un événement pour un contrat signé ;
* seul le support assigné peut modifier son événement ;
* seul le management peut assigner un support à un événement.

### Validation des données

Les entrées utilisateur sont validées dans :

```text
epic_events/validators.py
```

Les validations portent notamment sur :

* le format email ;
* le format téléphone français ;
* les montants positifs ;
* le montant restant qui ne doit pas dépasser le montant total ;
* les dates d'événement ;
* l'interdiction de créer un événement dans le passé ;
* le nombre de participants strictement positif ;
* les rôles autorisés.

### Gestion des erreurs SQL

Les erreurs d'intégrité de base de données, comme les emails ou numéros employés déjà existants, sont interceptées pour afficher un message métier compréhensible au lieu d'une erreur SQL brute.

## Journalisation avec Sentry

Sentry est initialisé au lancement de l'application si une variable `SENTRY_DSN` est définie.

Le fichier concerné est :

```text
epic_events/monitoring.py
```

L'application journalise notamment :

* les exceptions inattendues ;
* la création d'un collaborateur ;
* la modification d'un collaborateur ;
* la signature d'un contrat.

## Tests

Le projet contient des tests unitaires et fonctionnels.

Les tests couvrent notamment :

* le hash et la vérification des mots de passe ;
* les permissions par rôle ;
* la création et modification des clients ;
* la création et modification des contrats ;
* la création et modification des événements ;
* l'assignation du support ;
* l'authentification ;
* les tokens JWT ;
* les validators.

Lancer les tests :

```bash
poetry run pytest
```

## Qualité du code

Le projet utilise :

* Black pour le formatage ;
* Flake8 pour la vérification du style ;
* Pytest pour les tests.

Commandes utiles :

```bash
poetry run black .
poetry run flake8
poetry run pytest
```

## Données sensibles

Les fichiers suivants ne doivent pas être versionnés :

```text
.env
.venv/
__pycache__/
.pytest_cache/
*.pyc
```

Le fichier `.gitignore` doit contenir au minimum :

```gitignore
.env
.venv/
__pycache__/
*/__pycache__/
.pytest_cache/
*.pyc
```

## Auteur

Aurélien Amorin

Projet réalisé dans le cadre de la formation OpenClassrooms - Développeur d'application Python.
