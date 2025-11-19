# Sommatif — Docker Compose

## Objectif
Créer une architecture Docker Compose comprenant :

1. **reverse-proxy** (Nginx) — point d’entrée unique sur le réseau.
2. **app** (Nginx statique) — sert une page simple (application web).
3. **whoami** — Utilisé l'image `containous/whoamiservice` HTTP renvoyant ses en-têtes, IP et hostname (bref, les infos de la requête http, juste pour le plaisir ;P)

Le reverse proxy doit router :

- `/app/` → **service app**
- `/whoami/` → **service whoami**

Le reverse proxy doit utilisé le port externe `1005` et `92` à l'interne.

Vous devez utiliser **des adresses IP fixes** pour chaque service sur un réseau Docker personnalisé. Le nom du réseau est `fire_net`.

> Tous les fichiers de configuration Nginx nécessaires sont déjà fournis.

> **Votre seule tâche consiste à écrire le fichier `docker-compose.yml`.**

---

## Structure fournie

```
exam-compose-nginx/
├─ docker-compose.yml        # corrigé
├─ reverse-proxy/
│  └─ nginx.conf
└─ app/
   ├─ conf/nginx.conf
   └─ index.html
```

---

## Résultats attendus

- `http://localehostOuIpDuConteneur:NuméroDuPort/app/` affiche la page de l’application.

![image](img/result_app.png)

---

- `http://localehostOuIpDuConteneur:NuméroDuPort/whoami/` retourne un JSON avec l’IP et le hostname du service whoami.

---

![image](img/result_whoami.png)

- Les services `app`, `whoami` et `reverse-proxy` sont tous sur le réseau `fire_net` avec les IP fixes configurées.
