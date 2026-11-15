# Batline

Plateforme universitaire de partage de documents (syllabus, TP, mémoires, TFC…)
organisés par **faculté → promotion → branche → catégorie**, avec un espace
de discussions.

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate          # met aussi à jour une ancienne base Django 1.11
python manage.py createsuperuser  # accès à /admin/
python manage.py runserver
```

Puis ouvrir http://127.0.0.1:8000/ (redirige vers `/batline/accueil/`).

## Pages principales

| URL | Rôle |
| --- | --- |
| `/batline/faculte/` | liste des facultés |
| `/batline/promotion/<id>/` | promotions d'une faculté |
| `/batline/branche/<id>/` | branches (cours) d'une promotion et leurs catégories |
| `/batline/fichier/<id>/` | documents d'une catégorie |
| `/batline/discussions/` | derniers posts |
| `/batline/new-post/`, `/batline/new-file/` | publier (connexion requise) |
| `/batline/register/`, `/batline/login/` | inscription / connexion |
| `/admin/` | administration |

## Configuration (variables d'environnement)

| Variable | Défaut | Production |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | clé de dev non sûre | **obligatoire** |
| `DJANGO_DEBUG` | `1` | `0` |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | votre domaine |
| `DJANGO_DB_PATH` | `db.sqlite3` | chemin de la base |

## Tests

```bash
python manage.py test web
```
