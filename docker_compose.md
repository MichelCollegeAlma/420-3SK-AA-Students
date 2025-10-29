# Introduction à Docker Compose

## Qu'est-ce que Docker Compose ?

**Docker Compose** est un outil qui permet de **définir et de gérer plusieurs conteneurs Docker** dans un seul fichier appelé `docker-compose.yml`.

Il est particulièrement utile lorsqu'une application a besoin de plusieurs services qui doivent fonctionner ensemble (par exemple : un site web, une base de données et un serveur cache).

---

## Pourquoi utiliser Docker Compose ?

Sans Docker Compose, vous devriez lancer manuellement chaque conteneur avec plusieurs options (`docker run -d -p ...`). Cela devient vite complexe.

Avec Docker Compose :

* tout est défini dans **un seul fichier YAML** ;
* une seule commande suffit pour démarrer tous les services ;
* les conteneurs communiquent entre eux via un **réseau Docker interne** ;
* il est facile de **monter des volumes** et de **configurer des variables d'environnement**.

---

## Structure d’un fichier `docker-compose.yml`

Voici la structure générale :

```yaml
version: '3'
services:
  service1:
    image: nom_image:version
    ports:
      - "port_local:port_conteneur"
    environment:
      - VARIABLE=valeur
    volumes:
      - ./dossier_local:/chemin_conteneur
  service2:
    image: autre_image
    depends_on:
      - service1
```

### Explication des sections

| Élément         | Description                                           |
|-----------------|-------------------------------------------------------|
| **version**     | Version du format Compose (souvent `3` ou `3.9`).     |
| **services**    | Liste des conteneurs à lancer.                        |
| **image**       | Image Docker utilisée pour le service.                |
| **ports**       | Mappage des ports entre la machine et le conteneur.   |
| **environment** | Variables d’environnement passées au conteneur.       |
| **volumes**     | Liens entre les fichiers locaux et ceux du conteneur. |
| **depends_on**  | Indique les dépendances entre services.               |

---

## Exemple simple : Nginx + MariaDB

Créons une application composée d’un serveur web et d’une base de données.

**Fichier : `docker-compose.yml`**

```yaml
version: '3.9'
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./site:/usr/share/nginx/html

  db:
    image: mariadb:latest
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: pass
    volumes:
      - ./db_data:/var/lib/mysql
```

**Explication :**

* `web` : serveur Nginx exposé sur le port 8080.
* `db` : base de données MariaDB avec un mot de passe root.
* Les volumes `./site` et `./db_data` permettent de conserver les données locales.

---

## Commandes de base Docker Compose

```bash
# Lancer tous les services
docker compose up -d

# Voir les conteneurs en cours
docker compose ps

# Consulter les logs
docker compose logs -f

# Arrêter les services
docker compose down

# Recréer un service après modification
docker compose up -d --build
```

---

## Réseau Docker interne

Lorsque vous utilisez Docker Compose, un **réseau privé** est automatiquement créé pour vos services.

Les conteneurs peuvent se joindre par le **nom du service**. Par exemple :

* Le conteneur `web` peut accéder à la base de données `db` via l’adresse `db:3306`.

Ceci évite de gérer les adresses IP manuellement.

---

## Exemple plus complet : PHP + Apache + MariaDB

**Fichier : `docker-compose.yml`**

```yaml
version: '3.9'
services:
  web:
    image: php:8.2-apache
    ports:
      - "8080:80"
    volumes:
      - ./www:/var/www/html
    depends_on:
      - db

  db:
    image: mariadb:10.11
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: site_db
      MYSQL_USER: user
      MYSQL_PASSWORD: pass
    volumes:
      - ./db_data:/var/lib/mysql
```

Placez vos fichiers PHP dans le dossier `www/`, puis lancez :

```bash
docker compose up -d
```

Accédez ensuite à votre site : **[http://localhost:8080](http://localhost:8080)**.

---

## Avantages pédagogiques

* Visualisation claire de l’architecture d’une application multi-services.
* Facilité pour les étudiants de reproduire un environnement complet.
* Adapté à l’apprentissage des bases de données, serveurs web et API.

---

## Résumé des commandes clés

| Objectif                   | Commande                       |
|----------------------------|--------------------------------|
| Lancer l'environnement     | `docker compose up -d`         |
| Arrêter et supprimer       | `docker compose down`          |
| Voir les logs              | `docker compose logs -f`       |
| Voir les conteneurs        | `docker compose ps`            |
| Recréer après modification | `docker compose up -d --build` |

---

### En bref

Docker Compose est un outil indispensable pour orchestrer facilement plusieurs conteneurs liés entre eux. Il permet d’automatiser la mise en place d’environnements complets (serveur web, base de données, API, etc.) avec un seul fichier et une seule commande.
