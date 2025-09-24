# Bonnes pratiques pour l’installation, la configuration et l’utilisation d’un serveur Ubuntu

Ce document présente les principales recommandations pour sécuriser, configurer et utiliser correctement un serveur Ubuntu en production ou en environnement pédagogique.

---

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

# Résumé

1. Installation minimale et sécurisée.  
2. Configuration réseau, utilisateurs et pare-feu dès le départ.  
3. Sécurisation avec SSH par clés, fail2ban et mises à jour automatiques.  
4. Gestion des services via `systemctl` et des paquets via `apt`.  
5. Surveillance des logs, espace disque et supervision automatisée.  
6. Utilisation prudente : documentation, automatisation et sauvegardes.  
