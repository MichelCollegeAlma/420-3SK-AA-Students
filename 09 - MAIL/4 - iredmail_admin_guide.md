# Guide d'administration iRedMail
## Configuration et gestion des comptes email

---

## Table des matières

1. [Accès à l'interface d'administration](#accès-à-linterface-dadministration)
2. [Tableau de bord administrateur](#tableau-de-bord-administrateur)
3. [Gestion des domaines](#gestion-des-domaines)
4. [Création de comptes utilisateurs](#création-de-comptes-utilisateurs)
5. [Gestion des utilisateurs existants](#gestion-des-utilisateurs-existants)
6. [Configuration des alias email](#configuration-des-alias-email)
7. [Listes de diffusion](#listes-de-diffusion)
8. [Quotas et limites](#quotas-et-limites)
9. [Accès utilisateur (Roundcube)](#accès-utilisateur-roundcube)
10. [Surveillance et logs](#surveillance-et-logs)
11. [Sauvegardes](#sauvegardes)

---

## Accès à l'interface d'administration

### Connexion à iRedAdmin

**URL d'accès :**
```
https://mail.formation.lan/iredadmin
```

**Identifiants administrateur :**
- **Utilisateur :** `postmaster@formation.lan`
- **Mot de passe :** `test`

### Première connexion

1. Ouvrez votre navigateur web
2. Accédez à `https://mail.formation.lan/iredadmin`
3. Acceptez l'avertissement de sécurité SSL (certificat auto-signé)
4. Entrez vos identifiants administrateur
5. Cliquez sur **Login**

⚠️ **Important :** Changez le mot de passe par défaut lors de la première connexion en production.

---

## Tableau de bord administrateur

Après connexion, vous accédez au tableau de bord principal qui affiche :

### Vue d'ensemble
- **Nombre de domaines** configurés
- **Nombre d'utilisateurs** total
- **Espace disque utilisé** par domaine
- **Statistiques récentes** (dernières connexions, emails envoyés/reçus)

### Menu principal

Le menu de navigation contient les sections suivantes :

- **System** : Informations système et paramètres globaux
- **Domains** : Gestion des domaines mail
- **Admins** : Gestion des administrateurs
- **Users** : Liste et gestion des utilisateurs
- **Aliases** : Gestion des alias email
- **Mailing Lists** : Création et gestion des listes de diffusion

---

## Gestion des domaines

### Voir les domaines existants

1. Cliquez sur **Domains** dans le menu principal
2. Vous verrez la liste de tous les domaines configurés
3. Par défaut, le domaine `formation.lan` est déjà créé

### Ajouter un nouveau domaine

Si vous souhaitez gérer plusieurs domaines mail :

1. Cliquez sur **Domains** → **Add Domain**
2. Remplissez le formulaire :
   - **Domain name :** `exemple.lan` (nom du nouveau domaine)
   - **Description :** Description du domaine (optionnel)
   - **Default Quota :** Quota par défaut pour les utilisateurs (ex: 1024 MB)
   - **Max users :** Nombre maximum d'utilisateurs (0 = illimité)
3. Cliquez sur **Add**

### Modifier un domaine existant

1. Cliquez sur **Domains**
2. Cliquez sur le nom du domaine à modifier
3. Modifiez les paramètres souhaités :
   - Quota global du domaine
   - Nombre maximum d'utilisateurs
   - Paramètres de transport mail
4. Cliquez sur **Update** pour sauvegarder

### Supprimer un domaine

⚠️ **Attention :** Supprimer un domaine supprimera tous les utilisateurs et emails associés.

1. Cliquez sur **Domains**
2. Cochez la case du domaine à supprimer
3. Cliquez sur **Delete** en bas de page
4. Confirmez la suppression

---

## Création de comptes utilisateurs

### Méthode 1 : Via l'interface web iRedAdmin

**Étape 1 : Accéder à la création d'utilisateur**
1. Connectez-vous à iRedAdmin
2. Cliquez sur **Domains** dans le menu
3. Cliquez sur le nom du domaine (ex: `formation.lan`)
4. Cliquez sur l'onglet **Users**
5. Cliquez sur **Add User**

**Étape 2 : Remplir le formulaire**

**Informations obligatoires :**
- **Mail address :** `utilisateur1` (le @formation.lan sera ajouté automatiquement)
- **Password :** Mot de passe du compte
- **Confirm password :** Confirmer le mot de passe
- **Display name :** Nom complet de l'utilisateur (ex: "Jean Dupont")

**Informations optionnelles :**
- **Quota :** Espace disque alloué (MB) - ex: 1024 pour 1 GB
- **Job title :** Titre ou fonction
- **Telephone :** Numéro de téléphone
- **Mobile :** Numéro de mobile

**Étape 3 : Options avancées**

Dans la section **Advanced** :
- **Account status :** Active (coché) ou Disabled
- **Forwarding :** Transférer les emails vers une autre adresse
- **BCC :** Copie cachée de tous les emails reçus/envoyés

**Étape 4 : Créer le compte**
- Cliquez sur **Add** en bas du formulaire
- Le compte est créé immédiatement

### Méthode 2 : Via ligne de commande

Pour créer rapidement plusieurs utilisateurs :

```bash
# Se connecter au serveur en SSH
ssh test@mail.formation.lan

# Utiliser le script de création
sudo bash /opt/www/iredadmin/tools/create_mail_user_SQL.sh
```

Suivre les instructions interactives :
1. Entrer le domaine : `formation.lan`
2. Entrer le nom d'utilisateur : `utilisateur2`
3. Entrer le mot de passe
4. Confirmer le mot de passe

### Exemples d'utilisateurs à créer

Pour un environnement de formation, créez plusieurs comptes de test :

| Adresse email | Nom complet | Mot de passe | Quota |
|---------------|-------------|--------------|-------|
| jean.dupont@formation.lan | Jean Dupont | test123 | 1024 MB |
| marie.martin@formation.lan | Marie Martin | test123 | 1024 MB |
| support@formation.lan | Support Technique | test123 | 2048 MB |
| admin@formation.lan | Administrateur | test123 | 2048 MB |

---

## Gestion des utilisateurs existants

### Voir la liste des utilisateurs

1. Cliquez sur **Domains**
2. Cliquez sur le nom du domaine
3. L'onglet **Users** affiche tous les comptes

**Informations affichées :**
- Adresse email
- Nom complet
- Quota utilisé / Quota total
- Statut du compte (Actif/Désactivé)
- Date de création

### Modifier un utilisateur

1. Dans la liste des utilisateurs, cliquez sur l'adresse email
2. Vous pouvez modifier :
   - **Display name :** Nom affiché
   - **Password :** Changer le mot de passe
   - **Quota :** Augmenter/réduire l'espace disque
   - **Forwarding :** Redirection d'emails
   - **Account status :** Activer/désactiver le compte
3. Cliquez sur **Update** pour sauvegarder

### Réinitialiser un mot de passe

1. Cliquez sur l'adresse email de l'utilisateur
2. Dans la section **Password**, entrez le nouveau mot de passe
3. Confirmez le nouveau mot de passe
4. Cliquez sur **Update**

### Désactiver temporairement un compte

Plutôt que de supprimer un compte, vous pouvez le désactiver :

1. Cliquez sur l'adresse email de l'utilisateur
2. Décochez **Account Status : Active**
3. Cliquez sur **Update**

L'utilisateur ne pourra plus se connecter mais ses emails seront conservés.

### Supprimer un utilisateur

⚠️ **Attention :** La suppression est définitive et supprimera tous les emails.

1. Dans la liste des utilisateurs, cochez la case du compte à supprimer
2. Cliquez sur **Delete** en bas de page
3. Confirmez la suppression

---

## Configuration des alias email

Les alias permettent de créer des adresses email alternatives qui redirigent vers un ou plusieurs comptes existants.

### Créer un alias

**Exemple :** Créer `contact@formation.lan` qui redirige vers `support@formation.lan`

1. Cliquez sur **Domains**
2. Cliquez sur le domaine `formation.lan`
3. Cliquez sur l'onglet **Aliases**
4. Cliquez sur **Add Alias**

**Remplir le formulaire :**
- **Mail address :** `contact` (le @formation.lan sera ajouté automatiquement)
- **Display name :** "Contact général" (optionnel)
- **Redirect to :** `support@formation.lan`
- **Access policy :** Public (accepte les emails de tout le monde)

5. Cliquez sur **Add**

### Alias vers plusieurs destinataires

Pour rediriger vers plusieurs adresses :

**Exemple :** `info@formation.lan` → `admin@formation.lan` ET `support@formation.lan`

1. Dans le champ **Redirect to**, entrez les adresses séparées par des virgules :
   ```
   admin@formation.lan, support@formation.lan
   ```
2. Cliquez sur **Add**

### Cas d'usage courants

| Alias | Redirection vers | Usage |
|-------|------------------|-------|
| contact@formation.lan | support@formation.lan | Contact général |
| info@formation.lan | admin@formation.lan | Informations |
| ventes@formation.lan | commercial@formation.lan | Service commercial |
| abuse@formation.lan | postmaster@formation.lan | Signalement d'abus |
| noreply@formation.lan | /dev/null | Pas de réponse |

---

## Listes de diffusion

Les listes de diffusion permettent d'envoyer un email à plusieurs destinataires en une seule fois.

### Créer une liste de diffusion

**Exemple :** Créer `equipe@formation.lan` pour envoyer un email à toute l'équipe

1. Cliquez sur **Domains**
2. Cliquez sur le domaine `formation.lan`
3. Cliquez sur l'onglet **Mailing Lists**
4. Cliquez sur **Add Mailing List**

**Remplir le formulaire :**
- **Mail address :** `equipe`
- **Display name :** "Équipe Formation"
- **Access policy :** 
  - **Domain** : Seuls les membres du domaine peuvent envoyer
  - **Members only** : Seuls les membres de la liste peuvent envoyer
  - **Public** : N'importe qui peut envoyer

**Ajouter des membres :**
- Dans **Members**, ajoutez les adresses email une par ligne :
  ```
  jean.dupont@formation.lan
  marie.martin@formation.lan
  admin@formation.lan
  ```

5. Cliquez sur **Add**

### Modifier une liste de diffusion

1. Cliquez sur l'adresse de la liste
2. Ajoutez ou supprimez des membres
3. Modifiez la politique d'accès
4. Cliquez sur **Update**

### Cas d'usage

| Liste | Membres | Usage |
|-------|---------|-------|
| equipe@formation.lan | Tous les employés | Annonces générales |
| direction@formation.lan | Managers | Communications direction |
| support@formation.lan | Équipe support | Tickets support |
| dev@formation.lan | Développeurs | Discussions techniques |

---

## Quotas et limites

### Configurer les quotas par utilisateur

**Quota par défaut :** Défini au niveau du domaine (ex: 1024 MB)

**Modifier le quota d'un utilisateur :**
1. Cliquez sur l'adresse email de l'utilisateur
2. Dans **Quota**, entrez la nouvelle valeur en MB
   - 1024 MB = 1 GB
   - 2048 MB = 2 GB
   - 5120 MB = 5 GB
3. Cliquez sur **Update**

### Surveiller l'utilisation des quotas

1. Dans **Domains** → Nom du domaine → **Users**
2. La colonne **Quota** affiche l'utilisation actuelle :
   - `450 MB / 1024 MB` (44% utilisé)
   - Si un utilisateur atteint 100%, il ne peut plus recevoir d'emails

### Augmenter un quota

Si un utilisateur reçoit des erreurs "mailbox full" :

1. Accédez à son compte
2. Augmentez le quota (ex: de 1024 MB à 2048 MB)
3. Informez l'utilisateur de nettoyer régulièrement sa boîte

### Limites d'envoi

Pour éviter le spam, vous pouvez limiter le nombre d'emails envoyés :

**Configuration via iRedAPD :**
```bash
# Éditer la configuration
sudo nano /opt/iredapd/settings.py

# Ajouter/modifier ces lignes
THROTTLE_SETTING = {
    'user': {
        'msg_size': 10240,  # Taille max d'un email (KB)
        'max_msgs': 50,     # Nombre max d'emails par heure
        'max_quota': 100    # Quota total (MB) par heure
    }
}

# Redémarrer iRedAPD
sudo systemctl restart iredapd
```

---

## Accès utilisateur (Roundcube)

### URL d'accès

Les utilisateurs accèdent à leur webmail via :
```
https://mail.formation.lan/mail
```

### Connexion utilisateur

**Identifiants :**
- **Username :** Adresse email complète (ex: `jean.dupont@formation.lan`)
- **Password :** Mot de passe défini par l'administrateur

### Guide rapide pour les utilisateurs

**Envoyer un email :**
1. Cliquez sur **Compose** (Rédiger)
2. Entrez le destinataire dans **To**
3. Ajoutez un **Subject** (Sujet)
4. Rédigez le message
5. Cliquez sur **Send** (Envoyer)

**Lire les emails :**
- Les nouveaux emails apparaissent dans **Inbox** (Boîte de réception)
- Cliquez sur un email pour le lire
- Utilisez **Reply** pour répondre

**Organiser les emails :**
- Créez des dossiers via **Settings** → **Folders**
- Déplacez les emails par glisser-déposer

**Ajouter des contacts :**
1. Cliquez sur **Contacts** (Carnet d'adresses)
2. Cliquez sur **+** pour ajouter un contact
3. Remplissez les informations
4. Cliquez sur **Save**

**Paramètres utilisateur :**
1. Cliquez sur **Settings** (Paramètres)
2. Modifiez la langue, signature, filtres, etc.

### Configurer un client mail (Thunderbird, Outlook)

**Paramètres IMAP (recommandé) :**
- **Serveur IMAP :** `mail.formation.lan`
- **Port IMAP :** `993`
- **Sécurité :** `SSL/TLS`
- **Nom d'utilisateur :** `jean.dupont@formation.lan`
- **Mot de passe :** (mot de passe du compte)

**Paramètres SMTP (envoi) :**
- **Serveur SMTP :** `mail.formation.lan`
- **Port SMTP :** `587`
- **Sécurité :** `STARTTLS`
- **Authentification :** Oui (même identifiants)

**Paramètres POP3 (alternative) :**
- **Serveur POP3 :** `mail.formation.lan`
- **Port POP3 :** `995`
- **Sécurité :** `SSL/TLS`

⚠️ **Note :** IMAP est recommandé car il synchronise les emails sur tous les appareils.

---

## Surveillance et logs

### Surveiller l'activité mail

**Via l'interface iRedAdmin :**
1. Accédez au tableau de bord
2. Consultez les statistiques d'utilisation

**Via ligne de commande :**

**Voir les emails récents :**
```bash
# Logs Postfix (envoi/réception)
sudo tail -f /var/log/mail.log

# Filtrer par adresse email
sudo grep "jean.dupont@formation.lan" /var/log/mail.log
```

**Voir les connexions utilisateurs :**
```bash
# Logs Dovecot (IMAP/POP3)
sudo grep "dovecot" /var/log/mail.log | grep "Login"
```

**Vérifier les emails en file d'attente :**
```bash
# Voir la file d'attente
sudo postqueue -p

# Nombre d'emails en attente
sudo postqueue -p | tail -n 1
```

### Nettoyer la file d'attente

Si des emails sont bloqués :

```bash
# Forcer l'envoi des emails en attente
sudo postqueue -f

# Supprimer un email spécifique
sudo postsuper -d QUEUE_ID

# Supprimer tous les emails en attente
sudo postsuper -d ALL
```

### Vérifier l'état des services

```bash
# Vérifier tous les services
sudo systemctl status postfix dovecot nginx mariadb iredapd iredadmin php8.3-fpm

# Redémarrer un service si nécessaire
sudo systemctl restart postfix
```

---

## Sauvegardes

### Sauvegarder les données mail

**Emplacement des données importantes :**
- **Emails :** `/var/vmail/`
- **Base de données :** MariaDB
- **Configuration :** `/opt/iredmail/`, `/etc/postfix/`, `/etc/dovecot/`

### Script de sauvegarde automatique

**Créer un script de sauvegarde :**

```bash
# Créer le script
sudo nano /opt/backup_mail.sh
```

**Contenu du script :**
```bash
#!/bin/bash
BACKUP_DIR="/backup/iredmail"
DATE=$(date +%Y%m%d_%H%M%S)

# Créer le dossier de backup
mkdir -p $BACKUP_DIR

# Sauvegarder la base de données
mysqldump -u root -ptest --all-databases > $BACKUP_DIR/mysql_$DATE.sql

# Sauvegarder les emails
tar -czf $BACKUP_DIR/vmail_$DATE.tar.gz /var/vmail/

# Sauvegarder les configs
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /etc/postfix/ /etc/dovecot/ /opt/iredmail/

# Supprimer les sauvegardes de plus de 7 jours
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

**Rendre le script exécutable :**
```bash
sudo chmod +x /opt/backup_mail.sh
```

**Configurer une sauvegarde quotidienne :**
```bash
# Éditer le crontab root
sudo crontab -e

# Ajouter cette ligne pour une sauvegarde à 2h du matin
0 2 * * * /opt/backup_mail.sh
```

### Restaurer une sauvegarde

**Restaurer la base de données :**
```bash
mysql -u root -ptest < /backup/iredmail/mysql_YYYYMMDD_HHMMSS.sql
```

**Restaurer les emails :**
```bash
sudo tar -xzf /backup/iredmail/vmail_YYYYMMDD_HHMMSS.tar.gz -C /
sudo chown -R vmail:vmail /var/vmail/
```

---

## Bonnes pratiques

### Sécurité

1. **Changez les mots de passe par défaut** immédiatement
2. **Utilisez des mots de passe forts** pour tous les comptes
3. **Limitez les accès administrateurs** (principe du moindre privilège)
4. **Activez la surveillance** des logs régulièrement
5. **Mettez à jour** le système régulièrement

### Gestion quotidienne

1. **Vérifiez les quotas** des utilisateurs chaque semaine
2. **Surveillez la file d'attente** mail (doit être vide)
3. **Consultez les logs** pour détecter les anomalies
4. **Testez les sauvegardes** régulièrement
5. **Documentez** les changements de configuration

### Support utilisateurs

1. **Créez une documentation** simple pour les utilisateurs
2. **Formez les utilisateurs** à l'utilisation de Roundcube
3. **Définissez une procédure** pour les demandes de support
4. **Communiquez** les maintenances planifiées
5. **Collectez les retours** pour améliorer le service

---

## Dépannage courant

### Un utilisateur ne peut pas se connecter

**Vérifications :**
1. Le compte est-il actif ? (iRedAdmin → Users)
2. Le mot de passe est-il correct ?
3. Le quota est-il dépassé ?
4. Les services sont-ils démarrés ? (`systemctl status dovecot`)

### Les emails n'arrivent pas

**Vérifications :**
1. File d'attente : `sudo postqueue -p`
2. Logs Postfix : `sudo tail -f /var/log/mail.log`
3. DNS configuré correctement ?
4. Pare-feu ouvert sur les ports 25, 587, 465 ?

### Un utilisateur ne peut pas envoyer d'emails

**Vérifications :**
1. Authentification SMTP activée ?
2. Port 587 accessible ?
3. Quota d'envoi atteint ? (iRedAPD throttling)
4. Logs SMTP : `sudo grep "client=" /var/log/mail.log`

---

## Ressources supplémentaires

### Documentation officielle
- Site officiel : https://www.iredmail.org
- Documentation : https://docs.iredmail.org
- Forum : https://forum.iredmail.org

### Commandes utiles

```bash
# Recharger Postfix après modification
sudo postfix reload

# Tester la configuration Postfix
sudo postfix check

# Voir les connexions actives
sudo ss -tunap | grep -E ':25|:587|:143|:993'

# Statistiques emails
sudo pflogsumm /var/log/mail.log

# Espace disque utilisé par utilisateur
sudo du -sh /var/vmail/vmail1/formation.lan/*
```

---

## Conclusion

Ce guide couvre les tâches d'administration quotidiennes d'iRedMail. Pour des configurations avancées (antispam, antivirus, règles de filtrage), consultez la documentation officielle.

**Points clés à retenir :**
- Les utilisateurs accèdent à leur webmail via `https://mail.formation.lan/mail`
- Les administrateurs gèrent les comptes via `https://mail.formation.lan/iredadmin`
- Les sauvegardes automatiques sont essentielles
- La surveillance des logs permet de détecter les problèmes rapidement
- La documentation utilisateur facilite l'adoption du service

**Pour toute question ou assistance, consultez la documentation officielle ou le forum iRedMail.**