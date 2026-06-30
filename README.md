# 🏠 Airbnb Analytics Platform

## Présentation du projet

Plateforme analytique Airbnb construite avec une architecture Medallion (Bronze → Silver → Gold).
Ce projet analyse les logements, hôtes, avis clients et l'impact des nuits de pleine lune.

## Stack technique

| Outil     | Rôle                                     |
| --------- | ---------------------------------------- |
| DuckDB    | Moteur analytique local                  |
| dbt       | Transformations SQL (Bronze/Silver/Gold) |
| Streamlit | Dashboard interactif                     |
| GitHub    | Versioning                               |

## Architecture

## Installation

```bash
git clone https://github.com/barika-Ahlem/airbnb-analytics-platform.git
cd airbnb-analytics-platform
pip install dbt-duckdb duckdb streamlit pandas
```

## Exécution

```bash
# 1. Télécharger les données
cd data && bash download_data.sh && cd ..

# 2. Lancer le pipeline dbt complet
cd airbnb_dbt
dbt seed
dbt run
dbt test

# 3. Lancer le dashboard
cd ..
streamlit run app/streamlit_app.py
```

## Fonctionnalités

- 📋 **Analyse logements** : répartition par type, prix moyen, top 10
- 👤 **Analyse hôtes** : Superhost vs standard, top hôtes par listings
- 💬 **Analyse avis** : distribution sentiments, évolution temporelle, filtre par reviewer
- 🌕 **Pleine lune** : impact des nuits de pleine lune sur les sentiments

## Répartition des tâches

| Étape               | Responsable  |
| ------------------- | ------------ |
| Setup projet & Git  | Ahlem Barika |
| Couche Bronze       | Ahlem Barika |
| Couche Silver       | Eya BEN REJEB|
| Tests qualité       | Eya BEN REJEB|
| Couche Gold         | Ahlem Barika Eya BEN REJEB|
| Dashboard Streamlit | Ahlem Barika |
| Documentation       | Ahlem Barika Eya BEN REJEB|
