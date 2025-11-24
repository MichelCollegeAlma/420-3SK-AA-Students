# Théorie et architecture d'un serveur mail
## Comprendre iRedMail et son organisation

---

## Table des matières

1. [Introduction aux serveurs mail](#introduction-aux-serveurs-mail)
2. [Architecture d'un serveur mail complet](#architecture-dun-serveur-mail-complet)
3. [Les composants d'iRedMail](#les-composants-diredmail)
4. [Flux d'un email - Du point A au point B](#flux-dun-email---du-point-a-au-point-b)
5. [Pourquoi des tests en local ?](#pourquoi-des-tests-en-local)
6. [Organisation des fichiers sur le serveur](#organisation-des-fichiers-sur-le-serveur)
7. [Protocoles et ports utilisés](#protocoles-et-ports-utilisés)
8. [Sécurité et authentification](#sécurité-et-authentification)
9. [Gestion des domaines et utilisateurs](#gestion-des-domaines-et-utilisateurs)
10. [Différences : Environnement local vs Production](#différences--environnement-local-vs-production)

---

## Introduction aux serveurs mail

### Qu'est-ce qu'un serveur mail ?

Un **serveur mail** est un système informatique qui gère l'envoi, la réception, le stockage et la distribution des emails. Il fonctionne comme un bureau de poste numérique :

- **Envoi** : Accepte les emails des utilisateurs et les transmet au destinataire
- **Réception** : Reçoit les emails venant d'autres serveurs mail
- **Stockage** : Conserve les emails dans des boîtes aux lettres (mailboxes)
- **Distribution** : Permet aux utilisateurs d'accéder à leurs emails via différents protocoles

### Les trois rôles principaux

```
┌─────────────────────────────────────────────────────────────┐
│                    SERVEUR MAIL COMPLET                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MTA (Mail Transfer Agent) - Agent de Transport          │
│     → Postfix                                               │
│     → Envoie et reçoit des emails entre serveurs            │
│                                                             │
│  2. MDA (Mail Delivery Agent) - Agent de Livraison          │
│     → Dovecot LDA                                           │
│     → Délivre les emails dans les boîtes aux lettres        │
│                                                             │
│  3. MUA (Mail User Agent) - Agent Utilisateur               │
│     → Roundcube (webmail)                                   │
│     → Thunderbird, Outlook (clients)                        │
│     → Interface pour lire/envoyer des emails                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Qu'est-ce qu'iRedMail ?

**[iRedMail](https://www.iredmail.org/)** est une solution **tout-en-un** qui installe et configure automatiquement tous les composants nécessaires pour avoir un serveur mail complet et fonctionnel.

**Avantages :**
- ✅ Installation automatisée (gain de temps)
- ✅ Configuration optimisée (bonnes pratiques)
- ✅ Sécurité intégrée (SSL/TLS, authentification)
- ✅ Antivirus et antispam inclus
- ✅ Interface d'administration web
- ✅ Support de plusieurs backends (MySQL, PostgreSQL, LDAP)

**Sans iRedMail**, il faudrait installer et configurer manuellement chaque composant (plusieurs jours de travail).

---

## Architecture d'un serveur mail complet

### Vue d'ensemble de l'architecture iRedMail

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                │
└──────────────────────┬──────────────────────────────────────────┘
                       │ Ports 25, 587, 993, 443
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                    PARE-FEU / NFTABLES                          │
│  Ports autorisés: 25, 587, 143, 993, 80, 443, 10024, 10026      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
┌────────▼─────────┐        ┌────────▼─────────┐
│   NGINX (443)    │        │  POSTFIX (25)    │
│   Serveur Web    │        │  Serveur SMTP    │
│                  │        │                  │
│  - Roundcube     │        │  Envoi/Réception │
│  - iRedAdmin     │        │  d'emails        │
└────────┬─────────┘        └────────┬─────────┘
         │                           │
         │                  ┌────────▼─────────┐
         │                  │  AMAVIS (10024)  │
         │                  │  Filtrage        │
         │                  │                  │
         │                  │  ┌────────────┐  │
         │                  │  │  CLAMAV    │  │
         │                  │  │  Antivirus │  │
         │                  │  └────────────┘  │
         │                  │                  │
         │                  │  ┌────────────┐  │
         │                  │  │SpamAssassin│  │
         │                  │  │  Antispam  │  │
         │                  │  └────────────┘  │
         │                  └────────┬─────────┘
         │                           │
         │                  ┌────────▼─────────┐
         │                  │ DOVECOT (143)    │
         │                  │ Serveur IMAP     │
         │                  │                  │
         │                  │ Stockage emails  │
         │                  │ /var/vmail/      │
         │                  └────────┬─────────┘
         │                           │
         └───────────┬───────────────┘
                     │
            ┌────────▼─────────┐
            │   MARIADB        │
            │   Base de        │
            │   données        │
            │                  │
            │ - Utilisateurs   │
            │ - Domaines       │
            │ - Alias          │
            └──────────────────┘
```

---

## Les composants d'iRedMail

### 1. Postfix - Le MTA (Mail Transfer Agent)

**Rôle :** Serveur SMTP responsable de l'envoi et de la réception des emails

**Ports utilisés :**
- **Port 25** : SMTP (réception depuis d'autres serveurs mail)
- **Port 587** : SMTP Submission (envoi authentifié par les utilisateurs)
- **Port 465** : SMTPS (SMTP sécurisé - obsolète mais parfois utilisé)

**Fichiers de configuration :**
```
/etc/postfix/main.cf         # Configuration principale
/etc/postfix/master.cf       # Services et transports
/etc/postfix/mysql/          # Requêtes SQL pour les utilisateurs
```

**Responsabilités :**
- Accepter les emails des utilisateurs authentifiés
- Recevoir les emails venant d'autres serveurs
- Router les emails vers Amavis pour filtrage
- Transmettre les emails filtrés à Dovecot pour stockage
- Gérer la file d'attente des emails (`/var/spool/postfix/`)

---

### 2. Dovecot - Le serveur IMAP/POP3

**Rôle :** Permet aux utilisateurs d'accéder à leurs emails stockés

**Ports utilisés :**
- **Port 143** : IMAP (non sécurisé)
- **Port 993** : IMAPS (IMAP sécurisé via SSL/TLS)
- **Port 110** : POP3 (non sécurisé)
- **Port 995** : POP3S (POP3 sécurisé)

**Fichiers de configuration :**
```
/etc/dovecot/dovecot.conf              # Configuration principale
/etc/dovecot/conf.d/10-auth.conf       # Authentification
/etc/dovecot/conf.d/10-mail.conf       # Emplacement des mailboxes
/etc/dovecot/conf.d/10-master.conf     # Services et ports
```

**Responsabilités :**
- Authentifier les utilisateurs (SASL)
- Permettre l'accès aux emails via IMAP ou POP3
- Gérer les dossiers (Inbox, Sent, Trash, etc.)
- Livrer les nouveaux emails dans les boîtes (LDA - Local Delivery Agent)
- Indexer les emails pour la recherche rapide

**Différence IMAP vs POP3 :**

| Protocole | Stockage | Synchronisation | Usage |
|-----------|----------|-----------------|-------|
| **IMAP** | Sur le serveur | Tous les appareils | Recommandé (emails accessibles partout) |
| **POP3** | Téléchargé localement | Appareil unique | Ancien (emails supprimés du serveur) |

---

### 3. Amavis - Le filtre de contenu

**Rôle :** Filtrer les emails pour détecter les virus et le spam

**Ports utilisés :**
- **Port 10024** : Réception des emails depuis Postfix
- **Port 10026** : Renvoi des emails filtrés vers Postfix

**Fichiers de configuration :**
```
/etc/amavis/conf.d/50-user    # Configuration personnalisée
/var/lib/amavis/               # Données et fichiers temporaires
```

**Workflow :**
```
Email entrant → Postfix (25) 
    ↓
Amavis (10024) - Analyse antivirus (ClamAV) et antispam (SpamAssassin)
    ↓
Postfix (10026) - Email propre
    ↓
Dovecot - Livraison dans la boîte
```

---

### 4. ClamAV - L'antivirus

**Rôle :** Scanner les emails et pièces jointes pour détecter les virus

**Fichiers importants :**
```
/var/lib/clamav/               # Base de données des virus
/var/lib/clamav/main.cvd       # Signatures principales
/var/lib/clamav/daily.cld      # Mises à jour quotidiennes
/var/log/clamav/               # Logs de scan
```

**Mise à jour automatique :** `freshclam` télécharge les nouvelles signatures de virus quotidiennement

---

### 5. Nginx - Le serveur web

**Rôle :** Servir les interfaces web (Roundcube et iRedAdmin)

**Ports utilisés :**
- **Port 80** : HTTP (redirige vers HTTPS)
- **Port 443** : HTTPS (sécurisé)

**Fichiers de configuration :**
```
/etc/nginx/nginx.conf                    # Configuration principale
/etc/nginx/sites-enabled/                # Sites actifs
/etc/nginx/templates/                    # Templates iRedMail
```

**Applications hébergées :**
- **Roundcube** (`/opt/www/roundcubemail/`) : Webmail pour utilisateurs
- **iRedAdmin** (`/opt/www/iredadmin/`) : Interface d'administration

---

### 6. MariaDB/MySQL - La base de données

**Rôle :** Stocker les informations des utilisateurs, domaines, alias

**Port utilisé :**
- **Port 3306** : MySQL (accès local uniquement)

**Base de données principale :** `vmail`

**Tables importantes :**
```sql
vmail.mailbox     -- Comptes utilisateurs
vmail.domain      -- Domaines mail
vmail.alias       -- Alias et redirections
vmail.forwardings -- Transferts d'emails
```

**Exemple de structure :**
```
┌──────────────────────────┐
│   BASE DE DONNÉES vmail  │
├──────────────────────────┤
│                          │
│  TABLE: domain           │
│  - formation.lan         │
│                          │
│  TABLE: mailbox          │
│  - alice@formation.lan   │
│  - bob@formation.lan     │
│  - charlie@formation.lan │
│                          │
│  TABLE: alias            │
│  - equipe@formation.lan  │
│    → alice, bob          │
│                          │
└──────────────────────────┘
```

---

### 7. PHP-FPM - Le processeur PHP

**Rôle :** Exécuter le code PHP de Roundcube

**Port utilisé :**
- **Port 9999** : FastCGI (communication avec Nginx)

**Fichiers de configuration :**
```
/etc/php/8.3/fpm/php-fpm.conf
/etc/php/8.3/fpm/pool.d/www.conf
```

---

### 8. Roundcube - Le webmail

**Rôle :** Interface web pour que les utilisateurs lisent et envoient des emails

**Emplacement :** `/opt/www/roundcubemail/`

**Fichier de configuration :** `/opt/www/roundcubemail/config/config.inc.php`

**Connexions :**
- **IMAP** → Dovecot (port 143/993) pour lire les emails
- **SMTP** → Postfix (port 587) pour envoyer les emails

---

### 9. iRedAdmin - L'interface d'administration

**Rôle :** Interface web pour gérer les utilisateurs, domaines, quotas

**Emplacement :** `/opt/www/iredadmin/`

**Port utilisé :**
- **Port 7791** : uWSGI (serveur d'application Python)

**Connexions :**
- **Base de données** → MariaDB pour gérer les comptes

---

## Flux d'un email - Du point A au point B

### Scénario 1 : Envoi d'un email (Alice → Bob)

```
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 1 : Alice compose un email dans Roundcube                 │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 2 : Roundcube se connecte à Postfix (port 587)            │
│           Authentification SASL : alice@formation.lan           │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 3 : Postfix accepte l'email                               │
│           Message-ID assigné                                    │
│           Email ajouté à la file d'attente                      │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 4 : Postfix envoie l'email à Amavis (port 10024)          │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 5 : Amavis scanne l'email                                 │
│           - ClamAV vérifie les virus                            │
│           - SpamAssassin vérifie le spam                        │
│           - Résultat : "Passed CLEAN"                           │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 6 : Amavis renvoie l'email à Postfix (port 10026)         │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 7 : Postfix consulte la base de données                   │
│           Requête SQL : bob@formation.lan existe-t-il ?         │
│           MariaDB répond : Oui, maildir=/var/vmail/.../bob/     │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 8 : Postfix transmet à Dovecot LDA                        │
│           Dovecot écrit l'email dans /var/vmail/.../bob/new/    │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 9 : Email livré avec succès                               │
│           Statut : "status=sent (delivered to mailbox)"         │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 10 : Bob se connecte à Roundcube                          │
│            Roundcube se connecte à Dovecot (IMAP)               │
│            Dovecot lit /var/vmail/.../bob/new/                  │
│            L'email apparaît dans la boîte de réception          │
└─────────────────────────────────────────────────────────────────┘
```

**Temps total :** Moins d'une seconde pour un email local !

---

### Scénario 2 : Réception d'un email externe (Internet → Bob)

```
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 1 : Serveur externe (gmail.com) envoie un email           │
│           Requête DNS MX : formation.lan → mail.formation.lan   │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 2 : Connexion sur le port 25 de Postfix                   │
│           IP publique du serveur mail                           │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ ÉTAPE 3 : Postfix vérifie les politiques                        │
│           - SPF : Le serveur est-il autorisé ?                  │
│           - Greylisting : Première tentative ? (délai)          │
│           - iRedAPD : Vérifications supplémentaires             │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
          [ Même flux que précédemment ]
                    │
                    ▼
        Amavis → ClamAV → Dovecot → Mailbox
```

---

## Pourquoi des tests en local ?

### Limitations d'un domaine `.lan`

Le domaine `formation.lan` est un **domaine privé local** qui n'existe pas sur Internet.

**Conséquences :**
- ✅ **Fonctionne parfaitement en interne** : alice@formation.lan → bob@formation.lan
- ❌ **Ne peut pas recevoir d'emails d'Internet** : externe@gmail.com → test@formation.lan échouera
- ❌ **Ne peut pas envoyer d'emails vers Internet** (sera rejeté comme spam ou domaine inexistant)

### Pourquoi utiliser `.lan` pour la formation ?

**Avantages pédagogiques :**

1. **Environnement contrôlé**
   - Pas de dépendance à Internet
   - Pas de configuration DNS publique nécessaire
   - Pas de frais de domaine ou d'hébergement

2. **Sécurité**
   - Aucun risque d'envoyer des emails de test vers de vraies personnes
   - Isolation complète du réseau de production
   - Pas d'exposition publique du serveur

3. **Simplicité**
   - Configuration DNS minimale (fichier `/etc/hosts`)
   - Pas besoin de certificats SSL valides (auto-signés OK)
   - Focus sur l'apprentissage des concepts

4. **Coût zéro**
   - Pas d'achat de nom de domaine
   - Pas de frais d'hébergement
   - Infrastructure locale uniquement

### Ce que vous apprenez avec `.lan`

Même en environnement local, vous maîtrisez **tous les concepts essentiels** :

- ✅ Installation et configuration d'un serveur mail complet
- ✅ Gestion des utilisateurs et domaines
- ✅ Protocoles SMTP, IMAP, POP3
- ✅ Filtrage antivirus et antispam
- ✅ Authentification et sécurité
- ✅ Monitoring et logs
- ✅ Dépannage et résolution de problèmes

**La seule différence avec la production :** Pas de configuration DNS publique et pas de certificat SSL Let's Encrypt.

---

### Environnement local vs Production

| Aspect | Local (formation.lan) | Production (exemple.com) |
|--------|----------------------|--------------------------|
| **Domaine** | formation.lan (privé) | exemple.com (public) |
| **DNS** | /etc/hosts | DNS publics (MX, A, SPF, DKIM) |
| **Certificat SSL** | Auto-signé (avertissement) | Let's Encrypt (valide) |
| **IP** | 192.168.x.15 (privée) | IP publique |
| **Emails internes** | ✅ Fonctionne | ✅ Fonctionne |
| **Emails externes** | ❌ Impossible | ✅ Fonctionne |
| **Coût** | Gratuit | Domaine + hébergement |
| **Apprentissage** | ✅ Complet | ✅ Complet |

---

## Organisation des fichiers sur le serveur

### Structure globale

```
/
├── etc/                        # Fichiers de configuration
│   ├── postfix/                # Configuration Postfix
│   ├── dovecot/                # Configuration Dovecot
│   ├── amavis/                 # Configuration Amavis
│   ├── nginx/                  # Configuration Nginx
│   ├── php/                    # Configuration PHP
│   └── ssl/                    # Certificats SSL
│
├── opt/                        # Applications installées
│   ├── iredmail/               # Scripts iRedMail
│   ├── iredapd/                # iRedAPD (politiques)
│   └── www/                    # Applications web
│       ├── roundcubemail/      # Roundcube
│       └── iredadmin/          # iRedAdmin
│
├── var/                        # Données variables
│   ├── vmail/                  # Emails stockés (IMPORTANT!)
│   ├── log/                    # Fichiers de logs
│   ├── lib/                    # Données des applications
│   │   ├── amavis/             # Données Amavis
│   │   └── clamav/             # Base de données ClamAV
│   └── spool/                  # Files d'attente
│       └── postfix/            # File d'attente Postfix
│
└── usr/                        # Binaires et bibliothèques
    ├── sbin/                   # Exécutables système
    │   ├── postfix             # Binaire Postfix
    │   ├── dovecot             # Binaire Dovecot
    │   └── amavisd             # Binaire Amavis
    └── bin/                    # Exécutables utilisateurs
```

---

### Détails des emplacements importants

#### 1. Configuration Postfix

```
/etc/postfix/
├── main.cf                     # Configuration principale
├── master.cf                   # Services et transports
├── mysql/                      # Requêtes SQL
│   ├── virtual_mailbox_domains.cf      # Domaines virtuels
│   ├── virtual_mailbox_maps.cf         # Utilisateurs
│   └── virtual_alias_maps.cf           # Alias
├── sender_access                # Contrôle des expéditeurs
└── recipient_access            # Contrôle des destinataires
```

**Fichier clé : `main.cf`**
```bash
# Voir la configuration Postfix
sudo postconf | less

# Rechercher un paramètre spécifique
sudo postconf | grep mydomain
```

---

#### 2. Configuration Dovecot

```
/etc/dovecot/
├── dovecot.conf                # Configuration principale
├── conf.d/                     # Configurations par thème
│   ├── 10-auth.conf            # Authentification
│   ├── 10-mail.conf            # Emplacement des emails
│   ├── 10-master.conf          # Services et ports
│   ├── 10-ssl.conf             # Configuration SSL
│   ├── 20-imap.conf            # Paramètres IMAP
│   └── 20-pop3.conf            # Paramètres POP3
└── dovecot-sql.conf.ext        # Connexion base de données
```

**Paramètres importants :**
```bash
# Emplacement des mailboxes
mail_location = maildir:/var/vmail/vmail1/%d/%n/Maildir

# %d = domaine (formation.lan)
# %n = nom d'utilisateur (alice)
# Résultat : /var/vmail/vmail1/formation.lan/alice/Maildir
```

---

#### 3. Stockage des emails

```
/var/vmail/
└── vmail1/                     # Partition principale
    └── formation.lan/          # Domaine
        ├── a/l/i/              # Hachage du nom
        │   └── alice-2024.../  # Répertoire utilisateur
        │       └── Maildir/    # Format Maildir
        │           ├── new/    # Nouveaux emails non lus
        │           ├── cur/    # Emails lus
        │           ├── tmp/    # Temporaire
        │           └── .Sent/  # Dossier envoyés
        ├── b/o/b/
        │   └── bob-2024.../
        └── c/h/a/
            └── charlie-2024.../
```

**Format Maildir :**
- Chaque email = 1 fichier
- Avantage : Pas de corruption si un fichier est endommagé
- Nom du fichier : timestamp.unique.hostname

**Exemple de nom de fichier :**
```
1728566400.V801I40bd8M123456.mail.formation.lan,S=1234:2,S
```
- `1728566400` : Timestamp Unix
- `V801I40bd8` : Identifiant unique
- `S=1234` : Taille en bytes
- `:2,S` : Flags (S = vu/read)

---

#### 4. Logs système

```
/var/log/
├── mail.log                    # Tous les logs mail (principal)
├── mail.err                    # Erreurs mail uniquement
├── syslog                      # Logs système généraux
├── nginx/
│   ├── access.log              # Accès web
│   └── error.log               # Erreurs web
├── clamav/
│   └── clamav.log              # Scans antivirus
└── mysql/
    └── error.log               # Erreurs base de données
```

**Commandes utiles pour les logs :**
```bash
# Suivre les logs en temps réel
sudo tail -f /var/log/mail.log

# Voir les 100 dernières lignes
sudo tail -100 /var/log/mail.log

# Rechercher un utilisateur spécifique
sudo grep "alice@formation.lan" /var/log/mail.log

# Filtrer les erreurs uniquement
sudo grep -i error /var/log/mail.log

# Logs d'aujourd'hui seulement
sudo grep "$(date +%b\ %d)" /var/log/mail.log
```

---

#### 5. Base de données

**Emplacement des données :** `/var/lib/mysql/`

**Connexion :**
```bash
sudo mysql -u root -ptest
```

**Structure de la base vmail :**
```sql
USE vmail;

-- Voir toutes les tables
SHOW TABLES;

-- Structure de la table mailbox
DESCRIBE mailbox;

-- Lister tous les utilisateurs
SELECT username, domain, quota, active FROM mailbox;

-- Voir les alias
SELECT address, goto FROM alias;
```

---

#### 6. Applications web

```
/opt/www/
├── roundcubemail/              # Webmail
│   ├── config/
│   │   └── config.inc.php      # Configuration Roundcube
│   ├── logs/                   # Logs Roundcube
│   ├── temp/                   # Fichiers temporaires
│   └── plugins/                # Extensions
│
└── iredadmin/                  # Interface admin
    ├── settings.py             # Configuration iRedAdmin
    ├── libs/                   # Bibliothèques Python
    └── tools/                  # Scripts utilitaires
```

---

#### 7. Certificats SSL

```
/etc/ssl/
├── certs/
│   └── iRedMail.crt            # Certificat public
└── private/
    └── iRedMail.key            # Clé privée (protégée)
```

**En production avec Let's Encrypt :**
```
/etc/letsencrypt/
├── live/
│   └── mail.exemple