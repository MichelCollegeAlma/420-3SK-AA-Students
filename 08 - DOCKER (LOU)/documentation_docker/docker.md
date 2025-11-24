# Introduction à Docker

## Qu'est-ce que Docker ?

**Docker** est une plateforme permettant d'exécuter des applications dans des **conteneurs**. Un conteneur regroupe le code, les bibliothèques et les dépendances nécessaires à l'exécution d'une application, garantissant qu'elle fonctionne de la même manière sur n'importe quelle machine.

### Différence entre machine virtuelle et conteneur

| Machine virtuelle                          | Conteneur                        |
| ------------------------------------------ | -------------------------------- |
| Contient un système d'exploitation complet | Partage le noyau du système hôte |
| Plus lourd et lent à démarrer              | Léger et rapide                  |
| Isolation totale                           | Isolation par processus          |

---

## Pourquoi utiliser Docker ?

* **Isolation** : chaque application tourne dans un environnement séparé.
* **Portabilité** : le conteneur fonctionne partout (Windows, Linux, macOS, serveur).
* **Reproductibilité** : le code et les dépendances sont packagés ensemble.
* **Déploiement rapide** : prêt à exécuter en quelques secondes.
* **Automatisation** : utile pour les environnements de développement et de production.

---

## 3. Concepts de base

| Terme          | Description                                          | Exemple                                          |
|----------------|------------------------------------------------------|--------------------------------------------------|
| **Image**      | Modèle de conteneur, comme un fichier ISO            | `ubuntu:24.04`                                   |
| **Conteneur**  | Instance exécutée d'une image                        | `mon_conteneur`                                  |
| **Dockerfile** | Fichier texte décrivant comment construire une image | `FROM`, `RUN`, `COPY`                            |
| **Docker Hub** | Registre public d'images partagées                   | [https://hub.docker.com](https://hub.docker.com) |

---

## Commandes de base

```bash
# Vérifier la version
 docker --version

# Télécharger une image
 docker pull ubuntu:24.04

# Lister les images locales
 docker images

# Créer et lancer un conteneur interactif
 docker run -it ubuntu:24.04 bash

# Lister les conteneurs actifs
 docker ps

# Lister tous les conteneurs (même arrêtés)
 docker ps -a

# Arrêter un conteneur
 docker stop nom_du_conteneur

# Supprimer un conteneur
 docker rm nom_du_conteneur

# Supprimer une image
 docker rmi nom_de_l_image
```

---

## Exemple pratique : serveur web Nginx

```bash
# Télécharger et lancer Nginx sur le port 8080
docker run -d -p 8080:80 nginx
```

Explications :

* `-d` : mode détaché (en arrière-plan)
* `-p 8080:80` : redirige le port 80 du conteneur vers le port 8080 de la machine
* `nginx` : image utilisée

Accédez à **[http://localhost:8080](http://localhost:8080)** dans votre navigateur.

---

## Créer sa propre image avec un Dockerfile

**Exemple :** serveur web avec page personnalisée.

```dockerfile
FROM nginx:latest
COPY index.html /usr/share/nginx/html/index.html
```

Construction et exécution :

```bash
# Construire l'image
docker build -t mon_site_web .

# Lancer le conteneur
docker run -d -p 8080:80 mon_site_web
```
---

## 8. Récapitulatif

| Objectif                           | Commande ou fichier           |
| ---------------------------------- | ----------------------------- |
| Télécharger une image              | `docker pull`                 |
| Créer un conteneur                 | `docker run`                  |
| Lister les conteneurs              | `docker ps`                   |
| Arrêter / Supprimer                | `docker stop` / `docker rm`   |
| Construire une image personnalisée | `Dockerfile` + `docker build` |
| Orchestrer plusieurs conteneurs    | `docker-compose.yml`          |

---

### En bref

Docker simplifie l'exécution, le test et le déploiement d'applications en isolant les environnements.

Il est devenu un outil incontournable pour les développeurs, les administrateurs systèmes et les enseignants en informatique.
