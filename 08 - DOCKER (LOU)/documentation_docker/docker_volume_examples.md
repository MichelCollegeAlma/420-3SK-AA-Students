## Persistance et partage des données avec les volumes

### Schéma général

```
                ┌─────────────────────┐
                │    Fichiers locaux  │
                │  ./site/index.html  │
                └────────┬────────────┘
                         │ bind mount
                         ▼
    ┌──────────────────────────────────────────┐
    │              Conteneur Nginx             │
    │------------------------------------------│
    │ /usr/share/nginx/html/index.html         │
    └──────────────────────────────────────────┘
```

**Fichier Compose :**

```yaml
services:
  web:
    image: nginx
    volumes:
      - ./site:/usr/share/nginx/html:ro
```

* Le dossier `./site` de la machine hôte est monté **dans le conteneur**.
* L’option `:ro` rend le volume **lecture seule**.

### Volume nommé (données persistantes)

```
services:
  db:
    image: mariadb
    environment:
      MYSQL_ROOT_PASSWORD: secret
    volumes:
      - dbdata:/var/lib/mysql

volumes:
  dbdata: {}
```

**Fonctionnement :**

* Docker crée un volume nommé `dbdata`.
* Les données restent disponibles même si le conteneur `db` est supprimé.

### Volume temporaire en mémoire (tmpfs)

```
services:
  cache:
    image: redis
    volumes:
      - type: tmpfs
        target: /data
```

**Effet :**

* Les données dans `/data` ne sont jamais écrites sur le disque.
* Elles disparaissent dès que le conteneur s’arrête.

---

## Bonnes pratiques

**Volumes :**

* Utilisez des **bind mounts** pour le développement.
* Utilisez des **volumes nommés** pour les données persistantes (ex. bases SQL).
* Utilisez **tmpfs** pour les données sensibles ou temporaires.

---