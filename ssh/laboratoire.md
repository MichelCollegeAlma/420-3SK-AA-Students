
# Laboratoire — Clés SSH

---

## Objectifs d’apprentissage

À la fin de ce laboratoire, vous serez en mesure de :

1. Expliquer la différence entre une clé privée et une clé publique et leur rôle dans SSH.
2. Générer et gérer des clés SSH (ED25519 et RSA).
3. Comprendre la structure et les permissions du dossier `~/.ssh`.
4. Configurer une connexion SSH sans mot de passe.
5. Utiliser `ssh-agent` et le fichier `~/.ssh/config`.
6. Restreindre l’utilisation d’une clé avec les options de sécurité.
7. Identifier les clés d’hôte et le fichier `known_hosts`.

---

## 1. Préparation

- Installer **Docker Desktop** ou **Docker Engine**.
- Télécharger le fichier `docker-compose.yml` fourni.
- Ouvrir un terminal dans le dossier du laboratoire.

---

## 2. Simulation avec Docker Compose

Deux conteneurs simulant deux hôtes SSH :

| Conteneur  | Port | IP          | Utilisateur | Mot de passe |
|------------|------|-------------|-------------|--------------|
| clientPing | 2222 | 172.20.0.10 | clientPing  | clientPing   |
| clientPong | 2223 | 172.20.0.11 | clientPong  | clientPong   |

Utiliser l'image suivante : `lscr.io/linuxserver/openssh-server:latest`

### Lancer la simulation

```bash
docker compose up -d
docker compose ps
```

Tester les connexions :
```bash
ssh -p 2222 clientPing@172.20.0.10
ssh -p 2223 clientPong@172.20.0.11
```

---

## 3. Génération de paires de clés

Chaque client génère ses clés sur **sa machine locale**.

### Clé ED25519 (moderne)

```bash
ssh-keygen -t ed25519 -a 100 -C "prenom.nom@cours"
```

### Clé RSA (alternative compatible)

```bash
ssh-keygen -t rsa -b 4096 -C "prenom.nom@cours"
```

Les fichiers générés :

```
~/.ssh/id_ed25519        ← clé privée
~/.ssh/id_ed25519.pub    ← clé publique
```

---

## 4. Structure du dossier `.ssh`

| Fichier                     | Description                    | Permissions |
|-----------------------------|--------------------------------|-------------|
| id_ed25519 / id_rsa         | Clé privée (secrète)           | 600         |
| id_ed25519.pub / id_rsa.pub | Clé publique (diffusable)      | 644         |
| authorized_keys             | Clés publiques autorisées      | 600         |
| known_hosts                 | Empreintes des serveurs connus | 644         |
| config                      | Configuration du client SSH    | 644         |

Sous Windows : `C:\Users\<Nom>\.ssh\`

---

## 5. Échange de clés entre les clients

### clientPing → clientPong

```bash
ssh-copy-id -p 2223 -i ~/.ssh/id_ed25519.pub clientPong@172.20.0.10
```

### clientPong → clientPing

```bash
ssh-copy-id -p 2222 -i ~/.ssh/id_ed25519.pub clientPing@172.20.0.11
```

Test sans mot de passe :

```bash
ssh -p 2223 clientPong@172.20.0.10
ssh -p 2222 clientPing@172.20.0.11
```

Si ça fonctionne, l’authentification est réussie sans mot de passe.

---

## 6. Explication détaillée du fonctionnement de `ssh-copy-id`

1. Lecture de la clé publique locale (`~/.ssh/id_ed25519.pub`).
2. Connexion au serveur distant via mot de passe.
3. Création du dossier `~/.ssh` sur le serveur si besoin (permissions 700).
4. Ajout de la clé publique dans `~/.ssh/authorized_keys` (permissions 600).
5. Ajustement automatique des droits.
6. Confirmation : « Number of key(s) added: 1 ».

Lors de la prochaine connexion :
- Le client envoie sa clé publique.
- Le serveur vérifie sa présence dans `authorized_keys`.
- Si trouvée, il envoie un **défi cryptographique**.
- Le client signe ce défi avec sa clé privée.
- Le serveur vérifie la signature avec la clé publique.
- Si la signature est correcte, la connexion est établie **sans mot de passe**.

---

## 7. Options de sécurité `authorized_keys`

Dans le conteneur cible :

```
no-port-forwarding,no-agent-forwarding ssh-ed25519 AAAA... commentaire
```

Ces options empêchent les redirections de ports et renforcent la sécurité.

---

## 8. Utilisation de `ssh-agent`

`ssh-agent` conserve la clé déverrouillée en mémoire.

### Linux / macOS

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Windows

```powershell
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add "$env:USERPROFILE\.ssh\id_ed25519"
```

---

## 9. Fichier de configuration `~/.ssh/config`

### Exemple (clientPing et clientPong)

```
Host Ping
    HostName 172.20.0.10
    User clientPing
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 30
    ServerAliveCountMax 3

Host Pong
    HostName 172.20.0.11
    User clientPong
    Port 2223
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

### Détails des options principales

| Directive                      | Rôle                                   |
|--------------------------------|----------------------------------------|
| Host                           | Nom de l’alias utilisé dans `ssh Ping` |
| HostName                       | Adresse du serveur (ici `localhost`)   |
| User                           | Nom d’utilisateur distant              |
| Port                           | Port SSH (2222 ou 2223)                |
| IdentityFile                   | Fichier de clé privée à utiliser       |
| IdentitiesOnly yes             | Restreint aux clés listées             |
| ServerAliveInterval / CountMax | Maintient la session active            |

### Bonnes pratiques

- `IdentitiesOnly yes` pour éviter les erreurs d’authentification.
- `ForwardAgent no` (par défaut) pour éviter le transfert de clé.
- Vérifier les permissions (`~/.ssh` = 700, fichiers = 600).
- Garder un alias par machine pour éviter les erreurs.

### Vérification

```bash
ssh -G Ping | less   # Affiche la configuration effective
ssh -vvv Ping        # Mode verbeux pour le débogage
```

---

## 10. Désactiver l’accès par mot de passe

Quand tout fonctionne avec les clés :

1. Modifier le fichier `docker-compose.yml` :

```yaml
environment:
      - PASSWORD_ACCESS=false # Disables password login
```

2. Relancer :

```bash
docker compose up -d
```

Seules les connexions par clé publique resteront possibles.

---

## 11. Nettoyage

```bash
docker compose down -v
```

Supprime les conteneurs et leurs volumes (y compris les clés).

---

# Checklist de validation — Laboratoire SSH (clientPing / clientPong)

### Préparation
☐ Docker installé
☐ Fichier `docker-compose.yml` téléchargé
☐ Conteneurs lancés avec `docker compose up -d`
☐ Connexion testée à `clientPing` et `clientPong` via mot de passe

### Génération de clés
☐ Clé ED25519 générée avec `ssh-keygen -t ed25519`
☐ Clé RSA 4096 bits générée avec `ssh-keygen -t rsa -b 4096`
☐ Clés sauvegardées dans `~/.ssh/`
☐ Permissions correctes (`~/.ssh` = 700, `id_*` = 600, `id_*.pub` = 644)

### Échange de clés
☐ `ssh-copy-id` exécuté de clientPing → clientPong
☐ `ssh-copy-id` exécuté de clientPong → clientPing
☐ Connexion SSH réussie sans mot de passe dans les deux sens

### Vérification du fonctionnement
☐ Test de connexion : `ssh -vvv Ping`
☐ Clé présente dans `authorized_keys`
☐ Empreintes dans `known_hosts`

### Configuration `~/.ssh/config`
☐ Fichier créé avec Host Ping et Host Pong
☐ Tests `ssh Ping` et `ssh Pong` réussis

### Sécurité et agent
☐ `ssh-agent` configuré et clé ajoutée
☐ Restrictions ajoutées dans `authorized_keys`
☐ Accès par mot de passe désactivé

### Nettoyage
☐ `docker compose down -v` exécuté

---
