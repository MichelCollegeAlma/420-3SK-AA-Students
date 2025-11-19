# Exam Compose Nginx — Corrigé enseignant

Ce dossier contient une version **complète et fonctionnelle** de l’examen sur Docker Compose, avec :

- un **reverse proxy Nginx** (`reverse-proxy/nginx.conf`)
- un **site statique** servi par Nginx (`app/`)
- un service **whoami** (image `containous/whoami`)
- le fichier **`docker-compose.yml` corrigé**
- l’énoncé en Markdown (`examen-docker-compose-whoami.md`)

## Lancer l’architecture

```bash
docker compose up -d --build
docker compose ps
```

Puis tester :

- Application : http://localhost:8080/app/
- Whoami : http://localhost:8080/whoami/

Pour arrêter :

```bash
docker compose down
```
