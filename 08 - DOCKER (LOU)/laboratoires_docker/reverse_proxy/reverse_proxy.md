# Qu’est-ce qu’un Reverse Proxy ?

## Principe général

Un **reverse proxy** (ou **proxy inverse**) est un **serveur intermédiaire** placé entre les **clients (navigateurs web, applications)** et **un ou plusieurs serveurs internes**.
Il agit comme une **porte d’entrée unique** vers plusieurs services situés derrière lui.

### Sans reverse proxy
Chaque service web doit exposer **son propre port ou domaine** :
- `http://serveur1:8080`
- `http://serveur2:8081`
- `http://serveur3:8082`

Cela complique l’accès pour les utilisateurs et augmente la surface d’exposition sur Internet.

### Avec un reverse proxy
Le reverse proxy reçoit **toutes les requêtes HTTP** sur un **port unique (souvent 80 ou 443)** et les redirige **vers le bon serveur interne**, selon la configuration.

Exemple :
```
Client (navigateur)
        ↓
Reverse Proxy (Nginx)
        ↓
 ┌──────────────────────────────┐
 │ /app1 → serveur A :80        │
 │ /app2 → serveur B :80        │
 │ /api  → serveur C :5000      │
 └──────────────────────────────┘
```

Ainsi, le client ne connaît **qu’un seul point d’accès** :
`https://mon-serveur.com/app1`
`https://mon-serveur.com/app2`

---

## Rôle et utilités d’un reverse proxy

### 1. **Point d’entrée unique**
Le reverse proxy centralise toutes les requêtes.
Cela simplifie :
- la gestion des accès (pare-feu, sécurité),
- la configuration DNS (un seul domaine),
- et le routage interne.

### 2. **Répartition de charge (load balancing)**
Un reverse proxy peut distribuer les requêtes entre plusieurs serveurs identiques, améliorant la **performance** et la **tolérance aux pannes**.

Exemple :
```
upstream app_backend {
  server app1:80;
  server app2:80;
}
```

### 3. **Sécurité**
Le reverse proxy **masque les serveurs réels** (leurs adresses IP ne sont pas visibles).
Il peut aussi :
- filtrer certaines requêtes,
- gérer les **certificats HTTPS**,
- appliquer des règles d’accès.

### 4. **Mise en cache**
Il peut stocker des réponses pour réduire la charge des serveurs et accélérer les temps de réponse.

### 5. **Compression et optimisation**
Il peut compresser les réponses HTTP et optimiser le trafic entre client et serveur.

### 6. **Réécriture d’URL**
Il peut transformer les chemins d’accès pour offrir des URL cohérentes, comme :
`/app1/` → `http://serveur1.local/`
`/api/v1/` → `http://serveur2.local:5000/`

---

## Exemple concret (Nginx)

Configuration simple :

```nginx
server {
    listen 80;

    location /app1/ {
        proxy_pass http://app1:80/;
    }

    location /app2/ {
        proxy_pass http://app2:80/;
    }
}
```

Si l’utilisateur visite `http://localhost/app1/`,
le reverse proxy redirige la requête vers le conteneur `app1`.

---

## En résumé

| Fonction du reverse proxy | Description                                                              |
|---------------------------|--------------------------------------------------------------------------|
| **Routage**               | Redirige les requêtes vers le bon service.                               |
| **Sécurité**              | Masque les serveurs internes et gère HTTPS.                              |
| **Performance**           | Met en cache et répartit la charge.                                      |
| **Simplicité**            | Unifie l’accès via un seul domaine.                                      |
| **Maintenance**           | Permet d’ajouter/supprimer des serveurs sans perturber les utilisateurs. |
