# Exercice — Reverse Proxy Nginx avec Docker Compose

## Objectif
Créer une architecture à **3 services** à l’aide de Docker Compose :
1. `reverse-proxy` (Nginx) — point d’entrée unique
2. `frontend` (Nginx statique) — interface utilisateur
3. `api` (Flask) — API simple exposant `/api/health`, `/api/time` et `/api/echo`

Le reverse proxy doit router :
- `http://localhost:8080/app/` → **frontend**
- `http://localhost:8080/api/...` → **api**

> Tous les fichiers de configuration des services sont fournis.
> Votre seule tâche : **créer le fichier `docker-compose.yml`.**

---

## Structure du projet fournie

```
.
├─ reverse-proxy/
│  └─ nginx.conf
├─ frontend/
│  ├─ conf/nginx.conf
│  ├─ index.html
│  └─ app.js
└─ backend/
   ├─ Dockerfile
   └─ app.py
```

---

## Tâche à réaliser : `docker-compose.yml`

### Services à déclarer

#### 🔹 reverse-proxy
- Image : `nginx:alpine`
- Ports : **8080:80**
- Volume : ...
- Dépendances : `frontend`, `api`
- Réseau : `app_net`

#### 🔹 frontend
- Image : `nginx:alpine`
- Volumes :
  - ...
- Réseau : ...

#### 🔹 api
- Build : `./backend`
- Réseau : ...

#### 🔹 Réseau
- Créer un réseau `app_net` de type `bridge` partagé entre tous les services.

---

## Étapes de réalisation

- Créer le fichier **`docker-compose.yml`** à la racine du projet.
- Définir les **trois services** avec leurs paramètres (image, ports, volumes, depends_on…).
- Ajouter la **section réseau** en bas du fichier.
- Lancer le stack :
   ```bash
   docker compose up -d --build
   docker compose ps
   ```
- Vérifier que les trois conteneurs sont **Up**.
- Tester depuis un navigateur :
   - `http://localhost:8080/app/` → charge la page HTML.
   - Les boutons de la page envoient des requêtes à `/api/...`.
8. Tester l’API depuis le terminal :
   ```bash
   curl http://localhost:8080/api/health
   curl http://localhost:8080/api/time
   curl -X POST http://localhost:8080/api/echo -H "Content-Type: application/json" -d '{"message":"bonjour"}'
   ```
---

## Dépannage

### Erreur : *Connection refused sur localhost:8080*
→ Vérifiez que le **port 8080 est publié** dans `reverse-proxy`.

### Erreur : *Not Found sur /api/time*
→ Vérifiez le bloc `proxy_pass` du fichier `reverse-proxy/nginx.conf`.
Il doit être :
```nginx
location /api/ {
    proxy_pass http://api_upstream;  # sans slash à la fin
}
```

### Erreur : *frontend ne se charge pas*
→ Vérifiez les chemins exacts des volumes (`./frontend/index.html` etc.) et qu’ils existent bien.

---

## 💡 Astuce
Vous pouvez utiliser `docker compose logs -f` pour suivre les journaux des services en temps réel.

---
