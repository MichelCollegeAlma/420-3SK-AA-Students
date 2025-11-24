# Bonnes pratiques générales et spécifiques DNS

## 1) Installation du serveur

- **Télécharger uniquement depuis la source officielle** : utiliser les images ISO d’[Ubuntu](https://ubuntu.com/download/server).  
- **Vérifier l’intégrité** : comparer les checksums (`sha256sum`) de l’ISO avant installation.  
- **Partitionnement raisonné** : séparer `/`, `/home`, `/var` et `/tmp` si possible.  
- **Choisir SSH dès l’installation** si proposé, afin d’administrer le serveur à distance.  
- **Limiter les services installés** : n’installer que ce qui est nécessaire (éviter un serveur graphique par défaut).  

---

## 2) Configuration initiale

- **Mettre à jour immédiatement** après l’installation :
```bash
sudo apt update && sudo apt upgrade -y
```
- **Créer un utilisateur non-root** et utiliser `sudo` :
```bash
adduser admin
usermod -aG sudo admin
```
- **Désactiver la connexion root via SSH** pour limiter les attaques.  
- **Configurer l’adresse IP fixe** avec Netplan (`/etc/netplan/50-cloud-init.yaml`).  
- **Configurer un hostname explicite** (`/etc/hostname` et `/etc/hosts`).  
- **Activer le pare-feu (UFW)** :
```bash
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## 3) Sécurisation du serveur

- **Changer le port SSH par défaut** dans `/etc/ssh/sshd_config`.  
- **Utiliser des clés SSH** plutôt que des mots de passe :  
```bash
ssh-keygen -t ed25519
ssh-copy-id user@serveur
```
- **Installer `fail2ban`** pour bloquer les tentatives de connexion suspectes.  
- **Limiter les services exposés** : seuls les ports nécessaires doivent être ouverts (`ufw status`).  
- **Sauvegarder régulièrement** avec `rsync`, `scp` ou des outils de sauvegarde automatisés.  

---

## 4) Gestion des logiciels et services

- **Mettre en place des mises à jour automatiques** avec `unattended-upgrades`.  
- **Désinstaller les paquets inutiles** :
```bash
sudo apt autoremove --purge
```
- **Vérifier l’état des services** :
```bash
systemctl status apache2
systemctl status mysql
```
- **Contrôler l’espace disque** :
```bash
df -h
du -sh /var/log/*
```

---

## 5) Surveillance et maintenance

- **Analyser régulièrement les logs** : `/var/log/syslog`, `/var/log/auth.log`, `/var/log/apache2/`.  
- **Installer un outil de monitoring** (ex : `htop`, `atop`, `glances`).  
- **Configurer un service de supervision** (Nagios, Zabbix, Prometheus) pour surveiller la charge CPU, RAM, espace disque.  
- **Mettre en place un système d’alertes par mail** en cas de panne ou de seuil critique.  

---

## 6) Bonnes pratiques d’utilisation

- **Toujours utiliser `sudo`** plutôt que de se connecter en root.  
- **Ne pas installer de logiciels hors dépôts officiels** sauf si nécessaire (et vérifier leur signature).  
- **Documenter toutes les modifications** effectuées sur le serveur.  
- **Automatiser les tâches répétitives** avec des scripts Bash ou Ansible.  
- **Limiter le nombre d’utilisateurs** avec accès SSH.  
- **Faire des snapshots ou sauvegardes avant toute modification critique**.  

---



---

## 7) Bonnes pratiques spécifiques aux serveurs DNS (Bind9)

- **Séparer les rôles** : utiliser un serveur primaire pour la gestion des zones et un secondaire pour la redondance.  
- **Configurer des IP statiques** pour les serveurs DNS afin de garantir leur accessibilité.  
- **Limiter les transferts de zone** avec l’option `allow-transfer { <ip_secondaire>; };` afin que seuls les serveurs secondaires autorisés puissent répliquer les zones.  
- **Activer les notifications** (`notify yes;`) pour informer immédiatement les secondaires en cas de modification.  
- **Restreindre les requêtes externes** :  
```text
options {
    allow-query { trusted; };
    allow-recursion { trusted; };
    listen-on { 192.168.100.3; };
    listen-on-v6 { none; };
};
```
- **Protéger les zones** avec DNSSEC (`dnssec-validation auto;`).  
- **Sauvegarder régulièrement les fichiers de zones** (`/etc/bind/db.*`) et les conserver sous contrôle de version si possible.  
- **Vérifier la syntaxe après chaque modification** avec :  
```bash
named-checkconf -z
named-checkzone formation.lan /etc/bind/db.formation.lan
```
- **Automatiser les tests DNS** (via `dig` ou `nslookup`) après redémarrage du service.  
- **Configurer un fallback DNS** côté clients pour éviter une perte de résolution si le primaire tombe en panne.  
- **Surveiller les logs DNS** : `/var/log/syslog` contient les événements liés à Bind9.  
- **Limiter la taille du cache** pour éviter une consommation excessive de mémoire.  
- **Mettre à jour Bind9 régulièrement** pour corriger les failles de sécurité.  
- **Surveiller la réplication** entre primaire et secondaire en vérifiant les fichiers dans `/var/cache/bind/` du secondaire.  

---
