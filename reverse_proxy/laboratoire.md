# Laboratoire Docker Compose — Nginx Reverse Proxy + Plusieurs sites web

## 1. Contexte

Dans ce laboratoire, vous allez déployer une architecture avec **plusieurs sites web** derrière un **reverse proxy Nginx**.
L’utilisateur (navigateur) ne voit qu’une seule adresse (un seul port), mais Nginx redirige les requêtes vers différents conteneurs selon l’URL.

Vous utiliserez **Docker Compose** pour orchestrer l’ensemble.

---

## 2. Objectifs pédagogiques

1. Comprendre le rôle d’un **reverse proxy** HTTP.
2. Configurer **Nginx** pour router des requêtes vers différents services (routing par chemin : `/app1` et `/app2`).
3. Définir plusieurs services web dans un même fichier `docker-compose.yml`.
4. Utiliser des volumes pour monter des fichiers de configuration et des contenus statiques.
5. Ne publier qu’un seul port vers l’hôte (reverse proxy) tout en gardant les autres services accessibles uniquement sur le réseau interne Docker.

---

## 3. Prérequis

- Docker et Docker Compose installés.
- Connaissances de base sur :
  - Les conteneurs Docker (`docker run`, `docker ps`, etc.).
  - Le principe d’un serveur web (Nginx).
- Un éditeur de texte (VS Code, IntelliJ, Notepad++, etc.).

---

## 4. Architecture cible

Vous allez créer trois services :

- `reverse-proxy` : un Nginx configuré comme reverse proxy.
- `app1` : un site web statique (Nginx) accessible via le chemin `/app1`.
- `app2` : un autre site web statique (Nginx) accessible via le chemin `/app2`.

**Important :** Seul le service `reverse-proxy` expose un port vers l’extérieur (par ex. `8080:80`).
Les services `app1` et `app2` ne sont visibles que sur le réseau Docker.

Schéma logique (simplifié) :

- Navigateur → `http://localhost:8080/app1` → reverse-proxy → `app1`
- Navigateur → `http://localhost:8080/app2` → reverse-proxy → `app2`

---

## 5. Mise en place du projet

### 5.1. Structure des dossiers

Créez la structure suivante :

```text
labo-reverse-proxy/
├─ docker-compose.yml
├─ reverse-proxy/
│  └─ nginx.conf
├─ app1/
│  └─ index.html
└─ app2/
   └─ index.html
```

Commandes (sous Linux/macOS/WSL/PowerShell) :

```bash
mkdir -p labo-reverse-proxy/reverse-proxy
mkdir -p labo-reverse-proxy/app1
mkdir -p labo-reverse-proxy/app2
cd labo-reverse-proxy
```

Puis créez un fichier vide `docker-compose.yml` dans `labo-reverse-proxy`.

---

### 5.2. Contenu des sites `app1` et `app2`

Dans `app1/index.html`, mettez par exemple :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Application 1</title>
</head>
<body>
  <h1>Bienvenue sur Application 1</h1>
  <p>Ce contenu est servi par le conteneur <strong>app1</strong>.</p>
</body>
</html>
```

Dans `app2/index.html`, mettez par exemple :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Application 2</title>
</head>
<body>
  <h1>Bienvenue sur Application 2</h1>
  <p>Ce contenu est servi par le conteneur <strong>app2</strong>.</p>
</body>
</html>
```

Vous pouvez bien sûr personnaliser les textes/couleurs pour bien distinguer les deux applications.

---

## 6. Configuration du reverse proxy Nginx

### 6.1. Fichier `nginx.conf`

Dans le dossier `reverse-proxy`, créez un fichier `nginx.conf` contenant :

```nginx
user  nginx;
worker_processes  auto;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  65;

    # Log (optionnel, pour le débogage)
    access_log  /var/log/nginx/access.log;
    error_log   /var/log/nginx/error.log;

    # Upstreams (groupes de serveurs backend)
    upstream app1_backend {
        server app1:80;
    }

    upstream app2_backend {
        server app2:80;
    }

    server {
        listen 80;
        server_name _;

        # Page d'accueil simple (optionnelle)
        location = / {
            return 200 'Reverse proxy Nginx est en place. Utilisez /app1 ou /app2.';
            add_header Content-Type text/plain;
        }

        # Routage vers app1
        location /app1/ {
            proxy_pass http://app1_backend/;
        }

        # Routage vers app2
        location /app2/ {
            proxy_pass http://app2_backend/;
        }
    }
}
```

**Remarques :**

- Les noms `app1` et `app2` utilisés dans `server app1:80;` et `server app2:80;` correspondent aux **noms de services Docker Compose**.
- Le reverse proxy écoute sur le port `80` à l’intérieur du conteneur, mais sera publié vers l’hôte sur un autre port (par exemple `8080`).

---

## 7. Fichier `docker-compose.yml`

### 7.1. Exigences

Votre fichier `docker-compose.yml` doit :

1. Définir 3 services : `reverse-proxy`, `app1`, `app2`.
2. Utiliser l’image `nginx:alpine` pour les trois services.
3. Monter les volumes suivants :
   - `./reverse-proxy/nginx.conf` → `/etc/nginx/nginx.conf` (en lecture seule) pour `reverse-proxy`.
   - `./app1` → `/usr/share/nginx/html` (en lecture seule) pour `app1`.
   - `./app2` → `/usr/share/nginx/html` (en lecture seule) pour `app2`.
4. Exposer **uniquement** le service `reverse-proxy` vers l’hôte, sur le port `8080:80`.
5. Placer tous les services sur le même réseau applicatif (ex. `app_net`).

### 7.2. Travail demandé

1. Compléter le fichier `docker-compose.yml` pour respecter les exigences ci-dessus.
2. Lancer les services avec :

   ```bash
   docker compose up -d
   ```

3. Vérifier l’état des services :

   ```bash
   docker compose ps
   ```

4. Tester l’accès avec un navigateur :

   - `http://localhost:8080/` → message du reverse proxy.
   - `http://localhost:8080/app1/` → site `app1`.
   - `http://localhost:8080/app2/` → site `app2`.

5. Expérimenter :
   - Arrêter les services : `docker compose down`
   - Relancer : `docker compose up -d`
   - Modifier les pages HTML et recharger dans le navigateur.

---
