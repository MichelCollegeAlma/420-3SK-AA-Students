# Docker ports examples

---

## Communication par les ports

### Schéma général

```
┌───────────────────────────────────────────────┐
│                   HÔTE                        │
│-----------------------------------------------│
│   http://localhost:8080  →  [port 8080]       │
│                                               │
│   Docker mappe ce port vers :                 │
│      ↓                                        │
│   [port 80] dans le conteneur Nginx           │
└───────────────┬───────────────────────────────┘
                │
                │
                ▼
docker-compose.yml :
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

**Explication :**

* Le port **8080** est ouvert sur la machine hôte.
* Le port **80** est le port interne utilisé par le serveur Nginx.
* Toute requête vers `http://localhost:8080` est redirigée vers le conteneur Nginx.

### Ports internes uniquement

```
services:
  db:
    image: mariadb
    expose:
      - "3306"   # accessible seulement aux autres conteneurs
```

* `expose` permet à d’autres conteneurs du même réseau d’accéder au service sans exposer le port sur la machine hôte.

### Exemple multi-ports

```
services:
  app:
    image: myapp
    ports:
      - "80:80"      # HTTP
      - "443:443"    # HTTPS
      - "127.0.0.1:2222:22"  # SSH interne (loopback seulement)
```

---

## Bonnes pratiques

**Ports :**

* N’exposez que les ports nécessaires.
* Utilisez `expose` pour les communications internes.
* Précisez l’adresse locale (`127.0.0.1`) si le port ne doit pas être public.