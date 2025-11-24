# Installation d'iRedMail sur Ubuntu Server 24.04 LTS

## Prérequis

- VM Proxmox nommée "MAIL-US24" avec Ubuntu 24.04 LTS fraîchement installée
- Accès root ou sudo
- Adresse IP : 192.168.x.15
- Nom de domaine : mail.formation.lan
- Connexion Internet stable
- Espace disque : minimum 10 GB recommandé

## Étape 1 : Préparation du serveur

### Mettre à jour le système
```bash
sudo apt update && sudo apt upgrade -y
```

### Vérifier le nom d'hôte
```bash
hostnamectl
sudo hostnamectl set-hostname mail.formation.lan
```

Éditer `/etc/hosts` :
```bash
sudo nano /etc/hosts
```

Remplacer le contenu du fichier par :
```
127.0.0.1       localhost
127.0.0.1       mail.formation.lan mail
::1             localhost
::1             mail.formation.lan mail
192.168.x.15    mail.formation.lan mail
```

### Vérifier la configuration

Avant de continuer, vérifier que tout est correct :
```bash
cat /etc/hosts
hostname
hostname -f
```

Les commandes doivent retourner :
- `hostname` → `mail.formation.lan`
- `hostname -f` → `mail.formation.lan`

### Redémarrer pour appliquer les changements
```bash
sudo reboot
```

Après le redémarrage, vérifier à nouveau :
```bash
hostname -f
```

## Étape 2 : Télécharger et préparer iRedMail

### Obtenir la dernière version stable

Consultez la page officielle de téléchargement :
```
https://www.iredmail.org/download.html
```

Ou vérifiez les releases sur GitHub :
```
https://github.com/iredmail/iRedMail/releases
```

### Télécharger avec wget

Créer un répertoire pour l'installation :
```bash
mkdir -p ~/iRedMail-install
cd ~/iRedMail-install
```

Télécharger la dernière version stable (remplacer X.X.X par le numéro de version) :
```bash
wget https://github.com/iredmail/iRedMail/archive/refs/tags/X.X.X.tar.gz
```

**Exemple avec la version 1.7.3 (à vérifier sur le site officiel) :**
```bash
wget https://github.com/iredmail/iRedMail/archive/refs/tags/1.7.3.tar.gz
```

### Extraire l'archive et accéder au dossier

Extraire le fichier téléchargé :
```bash
tar xvf *.tar.gz
```

Accéder au dossier iRedMail :
```bash
cd iRedMail-*
```

Vérifier que vous êtes dans le bon répertoire :
```bash
pwd
ls -la
```

Vous devriez voir le fichier `iRedMail.sh`

## Étape 3 : Exécuter le script d'installation

### Lancer l'installateur
```bash
sudo bash iRedMail.sh
```

Le script lance un assistant interactif. Vous serez invité à configurer :

### Configuration proposée

**1. Chemin d'installation** (défaut : `/opt/iredmail`)
- Appuyez sur Entrée pour accepter le défaut

### 1. Chemin de stockage des emails
```
Default vmail directory: /var/vmail
```
➜ **Appuyez sur Entrée** pour accepter le chemin par défaut

### 2. Choix du serveur web
```
Which web server do you prefer?
1) Nginx (Recommanded)
2) Apache
```
➜ **Utilisez la flèche du bas** pour descendre sur **Nginx** (si pas déjà sélectionné)
➜ **Appuyez sur Espace** pour sélectionner
➜ **Appuyez sur Entrée** pour valider

**Note :** Nginx est recommandé - plus léger et performant

### 3. Choix de la base de données
```
Which backend do you prefer?
1) OpenLDAP
2) MariaDB (Recommanded)
3) PostgreSQL
```
➜ **Utilisez la flèche du bas** pour descendre sur **MariaDB**
➜ **Appuyez sur Espace** pour sélectionner
➜ **Appuyez sur Entrée** pour valider

**Note :** MariaDB est recommandé - le plus simple pour débuter

### 4. Mot de passe MySQL root
```
Please set a password for MySQL root user:
```
➜ **Entrez le mot de passe : test** et confirmez-le
   
⚠️ **Avertissement :** Dans un environnement de production, utilisez un mot de passe fort et complexe. Conservez ce mot de passe en lieu sûr !

### 5. Premier domaine mail
```
Please specify the first mail domain name:
```
➜ **Tapez : formation.lan** puis Entrée

### 6. Mot de passe de l'administrateur
```
Please set password for mail domain administrator: postmaster@formation.lan
```
➜ **Entrez le mot de passe : test** pour l'administrateur mail

⚠️ **Avertissement :** C'est le mot de passe pour accéder à l'interface iRedAdmin. Dans un environnement de production, utilisez un mot de passe fort et complexe.

### 7. Composants optionnels
```
Optional components:
[*] Roundcube webmail - Fast_and_lightweight_webmail
[ ] SOGo - Webmail,_Calendar,_Address_book,_ActiveSync
[*] netdata - Awesome_system_monitor
[*] iRedAdmin - Official_web-based_Admin_Panel
[*] Fail2ban - Ban_IP_with_too_many_password_failures
```

**Sélections recommandées pour la formation :**
- ✅ **[X] Roundcube webmail** - Interface webmail pour les utilisateurs (déjà coché par défaut)
- ✅ **[X] iRedAdmin** - Interface d'administration web (déjà coché par défaut)
- ✅ **[X] Fail2ban** - Protection contre les attaques par force brute (déjà coché par défaut)
- ✅ **[X] netdata** - Monitoring système (déjà coché par défaut)
- ⚠️ **[ ] SOGo Groupware** - Optionnel (calendrier/contacts/ActiveSync) - Consomme beaucoup de ressources

**Pour cet environnement de formation, garder tous les composants cochés par défaut.**

**Navigation :**
- Utilisez les **flèches haut/bas** pour vous déplacer
- Appuyez sur **Espace** pour cocher/décocher
- Appuyez sur **Tab** puis **Entrée** sur "OK" pour valider

**Note :** DKIM signing/verification et SPF validation sont activés par défaut. Les enregistrements DNS pour SPF et DKIM devront être configurés après l'installation.

### 8. Confirmation finale
```
*************************************************************************
* Below are the components will be installed:
*************************************************************************

[Informations affichées sur votre configuration]

Continue? [y|N]
```
➜ **Vérifiez attentivement** puis tapez **y** et Entrée pour continuer

### 9. Configuration du pare-feu (Firewall)
```
< Question > Would you like to use firewall rules provided by iRedMail?
< Question > File: /etc/nftables.conf, with SSHD ports: 22. [Y|n]
```

➜ **Tapez Y** puis Entrée pour accepter les règles de pare-feu iRedMail

**Explication :** iRedMail configurera automatiquement le pare-feu (nftables) avec les règles nécessaires pour :
- SSH (port 22)
- HTTP (port 80)
- HTTPS (port 443)
- SMTP (ports 25, 587)
- IMAP (ports 143, 993)
- POP3 (ports 110, 995)

**Important :** Si vous refusez (n), vous devrez configurer manuellement le pare-feu pour autoriser tous ces ports.

---

**L'installation va maintenant démarrer et prendra environ 15-30 minutes selon votre connexion Internet et les performances de la VM.**

## Étape 4 : L'installation

L'installateur va :
- Installer tous les paquets nécessaires
- Configurer le serveur web (Nginx)
- Configurer Postfix (SMTP)
- Configurer Dovecot (IMAP/POP3)
- Configurer la base de données (MariaDB)
- Configurer SSL/TLS automatiquement
- Initialiser iRedAdmin et Roundcube

## Étape 5 : Configuration post-installation

### Vérifier que l'installation est réussie

Vérifier que les services iRedMail sont actifs :
```bash
sudo systemctl status postfix
sudo systemctl status dovecot
sudo systemctl status nginx
sudo systemctl status mariadb
```

Tous les services doivent afficher **active (running)** en vert.

### Consulter le fichier iRedMail.tips

Le fichier `iRedMail.tips` contient toutes les informations importantes de votre installation.

**Note :** Le fichier est créé dans le **répertoire d'installation** (`~/iRedMail-install/iRedMail-*/`), pas dans `/root/`.

**Afficher le fichier :**
```bash
cat ~/iRedMail-install/iRedMail-*/iRedMail.tips
```

**Si la commande ci-dessus ne fonctionne pas**, rechercher le fichier :
```bash
find ~ -name "iRedMail.tips"
```

**Copier le fichier dans votre répertoire personnel :**
```bash
cp ~/iRedMail-install/iRedMail-*/iRedMail.tips ~/
```

Ce fichier contient :
- Les URLs d'accès aux interfaces web
- Les identifiants de connexion
- Les chemins de configuration importants
- Les commandes de gestion utiles

### Accéder aux interfaces web

Une fois l'installation terminée, vous pouvez accéder aux interfaces web depuis n'importe quel navigateur de votre réseau local.

**iRedAdmin (Interface d'administration)**
```
URL : https://mail.formation.lan/iredadmin
Utilisateur : postmaster@formation.lan
Mot de passe : test
```

Utilisez cette interface pour :
- Créer et gérer les comptes email
- Gérer les domaines
- Configurer les alias et listes de diffusion
- Consulter les logs

**Roundcube (Webmail pour les utilisateurs)**
```
URL : https://mail.formation.lan/mail
```

Les utilisateurs se connectent avec :
- Leur adresse email complète (ex: `utilisateur@formation.lan`)
- Leur mot de passe personnel

**Note :** Vous verrez un avertissement de sécurité SSL car le certificat est auto-signé. C'est normal pour un environnement de formation local.

## Étape 6 : Configuration DNS

Pour que votre serveur de mail fonctionne correctement dans votre réseau local, configurez les enregistrements sur votre serveur DNS local ou éditez directement les fichiers hosts des clients :

### Configuration locale (pour les clients du réseau LAN)

Sur votre serveur DNS ou machine client, ajouter dans `/etc/hosts` :
```
192.168.x.15  mail.formation.lan
```

### Records DNS recommandés (si DNS local configuré)

**A Record**
```
mail.formation.lan  A  192.168.x.15
```

**MX Record**
```
formation.lan  MX  10  mail.formation.lan
```

**SPF Record**
```
formation.lan  TXT  "v=spf1 mx -all"
```

### Note sur SSL/TLS en réseau local

Puisque vous utilisez un domaine `.lan` en réseau interne :
- iRedMail générera un certificat auto-signé
- Vous verrez un avertissement SSL dans le navigateur
- Pour l'environnement de formation, c'est acceptable
- Pour produire, utilisez un vrai domaine et Let's Encrypt

## Gestion des utilisateurs

### Via l'interface web iRedAdmin
1. Connectez-vous à https://mail.formation.lan/iredadmin
2. Allez dans Domain → Utilisateurs
3. Cliquez sur "Ajouter utilisateur"

### Via la ligne de commande
```bash
python /opt/iredmail/tools/create_mail_user_OpenLDAP.py
```

## Tâches de maintenance

### Sauvegardes automatiques
iRedMail inclut un script de sauvegarde. Configurez une tâche cron :

```bash
sudo crontab -e
```

Ajouter :
```
0 2 * * * /opt/iredmail/tools/backup_mysql.sh
```

### Certificat SSL/TLS
iRedMail utilise Let's Encrypt. Les certificats se renouvellent automatiquement.

Vérifier :
```bash
sudo certbot certificates
```

### Mettre à jour iRedMail
```bash
cd /opt/iredmail
sudo bash update_iredmail.sh
```

## Dépannage

### Impossible d'accéder aux interfaces web (ping fonctionne mais pas HTTPS)

Si vous pouvez faire un ping vers `mail.formation.lan` mais que les URLs https ne fonctionnent pas :

**1. Vérifier que Nginx est démarré :**
```bash
sudo systemctl status nginx
```

Si le service n'est pas actif :
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

**2. Vérifier que le pare-feu autorise les ports HTTP/HTTPS :**
```bash
sudo nft list ruleset | grep -E "80|443"
```

**Vérifier l'état de nftables :**
```bash
sudo systemctl status nftables
```

**Si nftables est actif, vérifier les tables existantes :**
```bash
sudo nft list tables
```

**Pour ajouter les règles, d'abord identifier la table correcte :**
```bash
# Afficher toute la configuration nftables
sudo nft list ruleset
```

**Si iRedMail a créé sa propre table, ajouter les règles :**
```bash
# Remplacer 'filter' par le nom de table correct (ex: 'inet iredmail')
sudo nft add rule inet iredmail input tcp dport 80 accept
sudo nft add rule inet iredmail input tcp dport 443 accept
```

**Solution plus simple - Désactiver temporairement le pare-feu pour tester :**
```bash
sudo systemctl stop nftables
sudo systemctl disable nftables
```

**Ou utiliser UFW si disponible :**
```bash
# Vérifier si UFW est installé
sudo ufw status

# Si UFW est actif
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

**3. Vérifier que Nginx écoute sur les bons ports :**
```bash
sudo ss -tlnp | grep -E ':80|:443'
```

Vous devriez voir Nginx écouter sur les ports 80 et 443.

**4. Tester l'accès local depuis le serveur :**
```bash
curl -k https://localhost/iredadmin
curl http://localhost/
```

**Si HTTP fonctionne mais pas HTTPS (Nginx n'écoute pas sur le port 443) :**

Cela signifie que Nginx n'a pas chargé la configuration SSL au démarrage.

**Solution simple - Redémarrer Nginx :**
```bash
# Vérifier que la configuration SSL existe et est activée
sudo ls -la /etc/nginx/sites-enabled/00-default-ssl.conf

# Vérifier que les certificats existent
sudo ls -la /etc/ssl/certs/iRedMail.crt
sudo ls -la /etc/ssl/private/iRedMail.key

# Tester la configuration Nginx
sudo nginx -t

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier que le port 443 est maintenant ouvert
sudo ss -tlnp | grep :443
```

Vous devriez voir Nginx écouter sur le port 443. Les interfaces web sont maintenant accessibles en HTTPS.

**Note :** Après l'installation d'iRedMail, si HTTPS ne fonctionne pas immédiatement, un simple redémarrage de Nginx suffit généralement à résoudre le problème.

**Si le problème persiste après le redémarrage :**

**Étape 1 : Vérifier la configuration Nginx :**
```bash
# Lister les sites disponibles
sudo ls -la /etc/nginx/sites-available/

# Vérifier le contenu du fichier de configuration principal
sudo cat /etc/nginx/sites-available/00-default-ssl.conf
```

**Étape 2 : Vérifier que le site SSL est activé :**
```bash
# Lister les sites activés
sudo ls -la /etc/nginx/sites-enabled/

# Si le lien symbolique SSL manque, le créer
sudo ln -s /etc/nginx/sites-available/00-default-ssl.conf /etc/nginx/sites-enabled/
```

**Étape 3 : Vérifier la configuration Nginx :**
```bash
sudo nginx -t
```

**Étape 4 : Vérifier les certificats SSL :**
```bash
sudo ls -la /etc/ssl/certs/iRedMail.crt
sudo ls -la /etc/ssl/private/iRedMail.key
```

**Si les certificats n'existent pas :**
```bash
# Générer un certificat auto-signé
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/iRedMail.key \
  -out /etc/ssl/certs/iRedMail.crt \
  -subj "/C=CA/ST=Quebec/L=Montreal/O=Formation/CN=mail.formation.lan"
```

**Étape 5 : Redémarrer Nginx :**
```bash
sudo systemctl restart nginx
sudo systemctl status nginx
```

**Étape 6 : Vérifier que le port 443 est maintenant ouvert :**
```bash
sudo ss -tlnp | grep :443
```

**Erreur 502 Bad Gateway :**

Cette erreur signifie que Nginx fonctionne mais ne peut pas communiquer avec les services backend (PHP-FPM, iRedAdmin, etc.).

**Solution complète - Démarrer tous les services nécessaires :**

```bash
# 1. Démarrer PHP-FPM (pour Roundcube)
sudo systemctl start php8.3-fpm
sudo systemctl enable php8.3-fpm

# 2. Démarrer iRedAPD (politique de filtrage mail)
sudo systemctl start iredapd
sudo systemctl enable iredapd

# 3. Démarrer iRedAdmin (interface d'administration)
sudo systemctl start iredadmin
sudo systemctl enable iredadmin

# 4. Redémarrer Nginx
sudo systemctl restart nginx

# 5. Vérifier que tous les services sont actifs
sudo systemctl status php8.3-fpm
sudo systemctl status iredapd
sudo systemctl status iredadmin
sudo systemctl status nginx
```

**Vérifier les ports :**
```bash
# Port 7791 pour iRedAdmin
sudo ss -tlnp | grep 7791

# Port 443 pour HTTPS
sudo ss -tlnp | grep 443
```

**Tester l'accès :**
```bash
curl -k https://localhost/iredadmin
curl -k https://localhost/mail/
```

Les deux doivent retourner du HTML (pas d'erreur 502).

**Note importante :** Après l'installation d'iRedMail, ces services doivent être démarrés manuellement la première fois, mais ils seront ensuite configurés pour démarrer automatiquement au boot.

**Roundcube (webmail) affiche une erreur 502 :**

Si Roundcube affiche "502 Bad Gateway", cela signifie que PHP-FPM n'écoute pas sur le bon port.

**Solution :**
```bash
# Redémarrer PHP-FPM pour appliquer la configuration
sudo systemctl restart php8.3-fpm

# Vérifier que PHP-FPM écoute sur le port 9999
sudo ss -tlnp | grep 9999

# Tester l'accès à Roundcube
curl -k https://localhost/mail/
```

Vous devriez maintenant voir la page de connexion Roundcube.

**Erreur 404 Not Found :**

Si vous obtenez une erreur 404 en HTTP, cela signifie que Nginx fonctionne mais la configuration des chemins est incorrecte. Vérifier :
```bash
# Vérifier la racine web
sudo nginx -T | grep root

# Vérifier les locations pour iredadmin et mail
sudo nginx -T | grep -A 5 "location.*iredadmin"
sudo nginx -T | grep -A 5 "location.*mail"
```

**Solution de contournement - Accès HTTP temporaire :**

En attendant de résoudre le problème HTTPS, vous pouvez accéder via HTTP :
```
http://mail.formation.lan/iredadmin
http://mail.formation.lan/mail
```

⚠️ **Attention :** HTTP n'est pas sécurisé, à utiliser uniquement pour tester en environnement de formation.

**5. Vérifier les logs Nginx :**
```bash
sudo tail -f /var/log/nginx/error.log
```

**Solution rapide pour Ubuntu avec UFW :**

Si UFW est actif au lieu de nftables :
```bash
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

### Erreur : "Please configure a fully qualified domain name (FQDN) in /etc/hosts"

Si vous recevez cette erreur lors du lancement de `sudo bash iRedMail.sh`, cela signifie que le FQDN n'est pas correctement configuré.

**Solution sans redémarrage :**

1. Vérifier le hostname actuel :
```bash
hostname -f
```

2. Changer le hostname sans redémarrer :
```bash
sudo hostnamectl set-hostname mail.formation.lan
sudo sysctl kernel.hostname=mail.formation.lan
```

3. Recharger la configuration du hostname dans le shell courant :
```bash
exec bash
```

4. Éditer `/etc/hosts` :
```bash
sudo nano /etc/hosts
```

S'assurer que le fichier contient exactement :
```
127.0.0.1       localhost
127.0.0.1       mail.formation.lan mail
::1             localhost
::1             mail.formation.lan mail
192.168.x.15    mail.formation.lan mail
```

5. Sauvegarder le fichier (Ctrl+O, Entrée, Ctrl+X)

6. Vérifier immédiatement :
```bash
hostname -f
cat /etc/hosts
```

Le résultat de `hostname -f` doit être `mail.formation.lan`

7. Relancer l'installation :
```bash
cd ~/iRedMail-install/iRedMail-*
sudo bash iRedMail.sh
```

**Points importants :**
- Le FQDN doit contenir au minimum un point (ex: `mail.formation.lan`)
- Le fichier `/etc/hosts` doit être modifié AVANT de lancer iRedMail.sh
- Les commandes `sysctl` et `exec bash` permettent d'appliquer le changement sans redémarrer

### Vérifier les logs
```bash
sudo tail -f /var/log/mail.log
sudo journalctl -u postfix -n 50
sudo journalctl -u dovecot -n 50
```

### Tester la connectivité
```bash
telnet mail.formation.lan 25
telnet mail.formation.lan 587
telnet mail.formation.lan 143
```

### Vérifier SPF/DKIM/DMARC
Utilisez un outil en ligne : mxtoolbox.com ou dmarcian.com

## Ports utilisants

- **25** : SMTP (réception)
- **587** : SMTP Submission (envoi)
- **143** : IMAP
- **993** : IMAP Sécurisé
- **110** : POP3
- **995** : POP3 Sécurisé
- **80** : HTTP
- **443** : HTTPS