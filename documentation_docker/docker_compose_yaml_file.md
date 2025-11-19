# Guide détaillé du fichier `docker-compose.yml`

> **Rappel** : avec Docker Desktop/Compose V2, la commande est `docker compose …` (sans tiret). Les spécifications ci‑dessous suivent la grammaire "Compose Specification" (ex‑V3).

---

## Squelette minimal et principes YAML

```yaml
# docker-compose.yml — squelette minimal
services:
  app:
    image: busybox:stable
    command: ["sh", "-c", "echo Hello && sleep 3600"]
```

* **YAML** : sensible aux indentations **espaces** (pas de tabulations), couples clé: valeur.
* Les **listes** se notent avec `- item` ou sous forme **JSON inline** `[a, b]`.
* Les **chaînes** peuvent être brutes (`valeur`), entre guillemets (`"valeur"`), ou multilignes (`|`).

---

## 2) Clés de haut niveau

| Clé                   | Rôle                                                              |
|-----------------------|-------------------------------------------------------------------|
| `services`            | Déclare chaque conteneur de l’application. **Obligatoire.**       |
| `volumes`             | (Optionnel) Déclare des **volumes nommés** réutilisables.         |
| `networks`            | (Optionnel) Déclare des **réseaux** personnalisés.                |
| `secrets` / `configs` | (Optionnel) Gestion de secrets/config (compat. Swarm et Compose). |

> Compose V2 n’impose plus `version:` (ex: `3.9`).

---

## Service : options les plus courantes

### `image`, `build`, `container_name`, `restart`

```yaml
services:
  web:
    image: nginx:1.27-alpine         # prend l’image publique
    container_name: demo-nginx       # nom lisible (sinon généré)
    restart: unless-stopped          # redémarrage automatique

  api:
    build:
      context: ./api                 # dossier contenant le Dockerfile
      dockerfile: Dockerfile.prod    # nom alternatif
      target: runtime                # stage cible (multi-stage)
      args:                          # ARG envoyés au build
        APP_ENV: production
```

**Notes** :

* `restart`: valeurs utiles — `no` (défaut), `on-failure`, `always`, `unless-stopped`.
* `build` et `image` peuvent coexister (l’image résultante est taguée automatiquement `project_service`), mais on préfère **l’un ou l’autre**.

### Réseau & ports : `ports`, `expose`, `networks`

```yaml
services:
  web:
    image: nginx:alpine
    ports:            # mappage hôte:conteneur
      - "8080:80"      # TCP par défaut
      - "127.0.0.1:8443:443" # bind sur loopback seulement
    expose:
      - "8081"         # visible par les autres services, pas par l’hôte
    networks:
      - frontnet
      - backnet

networks:
  frontnet: {}
  backnet:  {}
```

#### Comprendre les **ports**

Les **ports** permettent d’exposer un service Docker vers l’extérieur ou d’autoriser la communication entre conteneurs.

##### Exemple simple :

```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"   # <port_local>:<port_conteneur>
```

Ici, le port **80** à l’intérieur du conteneur (celui de Nginx) est accessible via le port **8080** de l’hôte. Vous pouvez donc visiter [http://localhost:8080](http://localhost:8080) pour voir votre serveur web.

##### Ports multiples et adresses spécifiques

```yaml
ports:
  - "8080:80"             # accessible sur toutes les interfaces
  - "127.0.0.1:9090:90"   # accessible seulement en local (loopback)
  - "443:443/tcp"         # protocole spécifié
```

##### Exposer un port sans le rendre public

```yaml
expose:
  - "3306"
```

`expose` rend le port visible uniquement **entre conteneurs du même réseau** Docker, mais pas depuis l’hôte. C’est utile pour les bases de données, par exemple.

##### Cas pratique :

```yaml
services:
  db:
    image: mariadb
    expose:
      - "3306"
  web:
    image: php:apache
    ports:
      - "8080:80"
    depends_on:
      - db
```

Le conteneur `web` pourra accéder à la base `db` via le port **3306**, même si ce port n’est pas exposé à l’extérieur.

> 💡 **Conseil :** évitez d’exposer inutilement des ports sensibles (comme 3306, 6379 ou 27017). Utilisez `expose` à la place lorsque possible.

---

### Variables : `environment`, `env_file`, substitution `.env`

```yaml
services:
  app:
    image: node:20-alpine
    environment:
      NODE_ENV: ${NODE_ENV:-development}  # défaut si non défini
      API_URL: http://api:8080
    env_file:                             # charge depuis un fichier
      - ./.env
```

* Fichier `.env` (au même niveau que `docker-compose.yml`) permet d’injecter des variables :

  ```dotenv
  NODE_ENV=production
  SECRET_TOKEN=s3cr3t
  ```
* Priorité : `environment` inline > `env_file` > `.env` du projet.

### Volumes : bind‑mount, nommés, `tmpfs`

```yaml
services:
  db:
    image: mariadb:11
    environment:
      MYSQL_ROOT_PASSWORD: exemple
    volumes:
      - dbdata:/var/lib/mysql           # volume **nommé** (persistant)
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro  # bind ro
      - type: tmpfs                     # données éphémères en RAM
        target: /tmp

volumes:
  dbdata: {}  # défini au niveau racine
```

#### Comprendre les **volumes**

Les **volumes** permettent de **conserver les données** même après la suppression des conteneurs. Ils peuvent aussi **lier** des dossiers de votre machine hôte à ceux des conteneurs.

##### Trois types de volumes

| Type             | Description                                      | Exemple                        |
|------------------|--------------------------------------------------|--------------------------------|
| **Volume nommé** | Géré par Docker, persistant entre redéploiements | `dbdata:/var/lib/mysql`        |
| **Bind mount**   | Monte un dossier local spécifique                | `./site:/usr/share/nginx/html` |
| **Tmpfs**        | Stocke des données temporaires en mémoire        | `type: tmpfs`                  |

##### Exemple pratique

```yaml
services:
  web:
    image: nginx
    volumes:
      - ./site:/usr/share/nginx/html   # bind : dossier du projet → conteneur
  db:
    image: mariadb
    environment:
      MYSQL_ROOT_PASSWORD: secret
    volumes:
      - dbdata:/var/lib/mysql          # volume nommé

volumes:
  dbdata: {}
```

* Le dossier local `./site` est monté dans le conteneur `web`, ce qui permet d’éditer les fichiers en direct.
* Le volume `dbdata` conserve les données de la base MariaDB même si le conteneur `db` est supprimé.

##### Volumes en lecture seule et multiples

```yaml
volumes:
  - ./config:/etc/nginx/conf.d:ro    # lecture seule
  - ./logs:/var/log/nginx            # un autre dossier monté
```

Le suffixe `:ro` rend le volume **read-only**. Très utile pour éviter qu’un service modifie des fichiers de configuration.

##### Volume tmpfs (RAM)

```yaml
volumes:
  - type: tmpfs
    target: /tmp/cache
```

Les données de `/tmp/cache` seront stockées en mémoire vive et disparaîtront à l’arrêt du conteneur.

##### Inspection et suppression

```bash
# Voir les volumes existants
docker volume ls

# Inspecter un volume
docker volume inspect dbdata

# Supprimer un volume inutilisé
docker volume prune
```

> 💡 **Conseil :** préférez les volumes nommés pour les données de base de données ou persistantes, et les bind mounts pour le développement (édition directe des fichiers du projet).

---

### Démarrage ordonné : `depends_on` + `healthcheck`

```yaml
services:
  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 10

  api:
    image: myorg/api:latest
    depends_on:
      db:
        condition: service_healthy     # attend la santé OK
```

> `depends_on.condition` fonctionne avec les **healthchecks**.

### Commande, entrée, utilisateur, dossier de travail

```yaml
services:
  worker:
    image: python:3.12-alpine
    working_dir: /app
    user: "1000:1000"                    # uid:gid
    volumes:
      - ./worker:/app
    entrypoint: ["python", "-m", "worker"] # remplace ENTRYPOINT
    command: ["--queue", "emails"]          # remplace CMD
```

### Limites et capacités : `deploy.resources` (locale) et `ulimits`

> En local (non‑Swarm), `deploy` est **partiellement** supporté par certains runtimes ; pour Compose, privilégiez `cpus`, `mem_limit` et `ulimits` au niveau service.

```yaml
services:
  cpu_job:
    image: busybox
    command: ["sh", "-c", "yes > /dev/null"]
    cpus: 1.5           # ≈ quotas CPU (Compose V2)
    mem_limit: 512m     # limite mémoire
    ulimits:
      nofile: 65535
```

### Logs, redémarrage, arrêt propre

```yaml
services:
  app:
    image: golang:1.22-alpine
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    stop_signal: SIGINT
    stop_grace_period: 15s
```
---

## Exemples multilayers prêts à copier

### LAMP minimal (Apache + PHP + MariaDB)

```yaml
services:
  web:
    image: php:8.3-apache
    ports: ["8080:80"]
    volumes:
      - ./www:/var/www/html
    depends_on:
      db:
        condition: service_started

  db:
    image: mariadb:11
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: app
      MYSQL_USER: app
      MYSQL_PASSWORD: app
    volumes:
      - dbdata:/var/lib/mysql

volumes:
  dbdata: {}
```

### Nginx en reverse‑proxy + deux backends

```yaml
services:
  reverse:
    image: nginx:alpine
    ports: ["80:80"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
      - frontend

  api:
    image: myorg/api:latest
    environment:
      DB_URL: postgres://postgres:postgres@db:5432/app

  frontend:
    image: node:20-alpine
    command: ["sh", "-c", "npm ci && npm run start"]
    working_dir: /app
    volumes: ["./frontend:/app"]

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: postgres

networks:
  default:
    name: appnet  # réseau unique commun aux services
```

### Profiles (dev vs prod) + overrides

```yaml
# docker-compose.yml (base)
services:
  api:
    build: { context: ./api }
    environment:
      LOG_LEVEL: info
    ports: ["8080:8080"]

---
# docker-compose.dev.yml
services:
  api:
    profiles: [dev]
    environment:
      LOG_LEVEL: debug
    volumes:
      - ./api:/app

---
# Commandes
# Dev :
#   docker compose -f docker-compose.yml -f docker-compose.dev.yml --profile dev up -d
# Prod (base seule) :
#   docker compose up -d
```

### Secrets & configs (fichiers sensibles)

```yaml
services:
  app:
    image: nginx:alpine
    secrets:
      - api_key
    configs:
      - site_conf

secrets:
  api_key:
    file: ./secrets/api_key.txt

configs:
  site_conf:
    file: ./nginx/site.conf
```

### Attendre la BD proprement (healthcheck + wait‑for)

```yaml
services:
  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 12

  migrator:
    image: flyway/flyway:10
    depends_on:
      db:
        condition: service_healthy
    command: -url=jdbc:postgresql://db:5432/postgres -user=postgres -password=postgres migrate
```

### Multi‑réseaux (front/back isolation)

```yaml
services:
  web:
    image: nginx:alpine
    ports: ["8080:80"]
    networks: [front]

  api:
    image: myorg/api
    networks: [front, back]

  db:
    image: postgres:16
    networks: [back]

networks:
  front: {}
  back: {}
```

---

## Fichiers, structure et workflow

```
project/
├─ docker-compose.yml
├─ docker-compose.dev.yml        # overrides (optionnel)
├─ .env                          # variables du projet
├─ secrets/                      # fichiers sensibles (git‑ignored)
├─ www/                          # sources web
└─ db_data/                      # volume bind local (dev)
```

**Cycle de vie type**

```bash
# Démarrer en arrière-plan
docker compose up -d

# Voir les conteneurs et leur état
docker compose ps

# Logs (stream)
docker compose logs -f api

# Exécuter une commande dans un conteneur
docker compose exec api sh

# Appliquer des changements d’image
docker compose up -d --build api

# Arrêter + supprimer conteneurs/réseaux (préserve volumes)
docker compose down

# Tout supprimer, y compris volumes nommés
docker compose down -v
```

---

## Sécurité & bonnes pratiques

* **Ne commitez pas** de secrets en clair : utilisez `secrets`, variables d’environnement hors VCS, coffre de secrets.
* Préférez des **images officielles, taguées** (`x.y` ou `x.y-alpine`) plutôt que `latest`.
* Ajoutez des **healthchecks** aux services critiques.
* Limitez les droits : `user:`, `read_only: true`, `cap_drop: [ALL]` puis `cap_add` au cas par cas.
* Surveillez les logs et **limitez leur taille** (`logging.options.max-size`).

---

## Dépannage rapide (FAQ)

* **Port déjà utilisé** : changez la partie **hôte** dans `ports` (`8081:80`).
* **Variables non prises en compte** : vérifiez `.env`, l’ordre des `-f` et la **priorité** (inline > env_file > .env).
* **BD non prête** : utilisez `healthcheck` + `depends_on.condition: service_healthy`.
* **Volumes qui ne persistent pas** : utilisez des **volumes nommés** au lieu de bind sur `/tmp`.
* **Différences Swarm/Compose** : évitez `deploy:` en local ; préférez `cpus`, `mem_limit`.

---

## Exemple « tout‑en‑un »

```yaml
# Exemple complet pour une appli web avec cache et migrations
services:
  web:
    image: nginx:1.27-alpine
    ports: ["80:80"]
    volumes:
      - ./deploy/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      api:
        condition: service_started
    networks: [front]

  api:
    build:
      context: ./api
      target: runtime
      args: { APP_ENV: production }
    environment:
      DB_URL: postgresql://postgres:postgres@db:5432/app
      REDIS_URL: redis://cache:6379
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks: [front, back]

  cache:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes"]
    volumes: ["cachedata:/data"]
    networks: [back]

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: postgres
    volumes:
      - dbdata:/var/lib/postgresql/data
    networks: [back]

  migrator:
    image: flyway/flyway:10
    depends_on:
      db:
        condition: service_healthy
    command: -url=jdbc:postgresql://db:5432/postgres -user=postgres -password=postgres migrate
    networks: [back]

volumes:
  dbdata: {}
  cachedata: {}

networks:
  front: {}
  back: {}
```
---