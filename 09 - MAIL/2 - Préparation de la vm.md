# 2. Préparation de la machine virtuelle

### 2.1 Créer la VM dans Proxmox

1. **Cloner votre VM de base Ubuntu Server 24.04** pour créer :
   - Nom de la VM : `MAIL-US24`
   - Template source : `Ubuntu-clean` (ou votre template de base)

2. **Configurer les ressources** (recommandé) :
   - **CPU** : 2 cœurs
   - **RAM** : 4 GB (minimum 2 GB)
   - **Disque** : 20 GB (minimum 10 GB)
   - **Réseau** : Bridge vers votre réseau local

### 2.2 Attribuer l'adresse IP statique

**Méthode 1 : Via Netplan (Ubuntu 24.04)**

Éditez le fichier de configuration réseau :
```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

**Contenu du fichier :**
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens18:  # Vérifiez le nom de votre interface avec 'ip a'
      addresses:
        - 192.168.100.15/24
      routes:
        - to: default
          via: 192.168.100.1  # Votre passerelle
      nameservers:
        addresses:
          - 192.168.100.5     # DNS primaire
        search:
          - formation.lan
```

**Appliquer la configuration :**
```bash
sudo netplan apply
```

**Vérifier la configuration :**
```bash
ip addr show
ip route show
```

### 2.3 Vérifier la connectivité réseau

```bash
# Ping vers la passerelle
ping -c 4 192.168.100.1

# Ping vers le DNS primaire
ping -c 4 192.168.100.3

# Ping vers Internet (si applicable)
ping -c 4 8.8.8.8

# Test de résolution DNS
ping -c 4 google.com
```

---

## 3. Configuration du nom d'hôte

### 3.1 Changer le nom d'hôte de la machine

```bash
sudo hostnamectl set-hostname mail
```

### 3.2 Vérifier le changement

```bash
hostnamectl
```

**Résultat attendu :**
```
   Static hostname: mail
         Icon name: computer-vm
           Chassis: vm
        Machine ID: ...
           Boot ID: ...
    Virtualization: kvm
  Operating System: Ubuntu 24.04 LTS
            Kernel: Linux 6.8.0-...
      Architecture: x86-64
```

---

## 4. Configuration du fichier /etc/hosts

### 4.1 Éditer le fichier hosts

```bash
sudo nano /etc/hosts
```

### 4.2 Configuration correcte du fichier

**Remplacer le contenu par :**
```
127.0.0.1       localhost
127.0.0.1       mail.formation.lan mail

# L'adresse IP locale de la machine
192.168.x.15    mail.formation.lan mail

# IPv6
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters
```

**⚠️ Points importants :**
- Le **FQDN complet** doit apparaître : `mail.formation.lan`
- Le **hostname court** doit suivre : `mail`
- L'**adresse IP locale** doit pointer vers le FQDN
- **Ne PAS mettre** l'IP 127.0.1.1 avec le hostname (erreur courante)

### 4.3 Sauvegarder et quitter

- Appuyez sur `Ctrl + O` pour sauvegarder
- Appuyez sur `Entrée` pour confirmer
- Appuyez sur `Ctrl + X` pour quitter

---

## 5. Validation de la configuration hostname et DNS

### 5.1 Vérifier le hostname

```bash
# Voir le hostname court
hostname

# Résultat attendu : mail
```

```bash
# Voir le FQDN complet
hostname -f

# Résultat attendu : mail.formation.lan
```

```bash
# Voir toutes les informations
hostnamectl

# Le Static hostname doit être : mail
```

### 5.2 Vérifier la résolution DNS locale

```bash
# Résolution du FQDN
ping -c 4 mail.formation.lan

# Résultat attendu :
# PING mail.formation.lan (192.168.x.15) 56(84) bytes of data.
# 64 bytes from mail.formation.lan (192.168.x.15): icmp_seq=1 ttl=64 time=0.025 ms
```

```bash
# Résolution via DNS
nslookup mail.formation.lan

# Résultat attendu :
# Server:         192.168.x.3
# Address:        192.168.x.3#53
#
# Name:   mail.formation.lan
# Address: 192.168.x.15
```

```bash
# Test avec dig (plus détaillé)
dig mail.formation.lan

# Vérifier la section ANSWER
```

### 5.3 Vérifier la résolution du domaine formation.lan

```bash
# Ping vers le domaine
ping -c 4 formation.lan

# Résultat attendu : doit résoudre vers une IP du réseau
```

```bash
# Ping vers d'autres machines du domaine
ping -c 4 primaire.formation.lan
ping -c 4 secondaire.formation.lan
ping -c 4 host1.formation.lan
```

---

## 6. Dépannage courant

### Problème 1 : Hostname non résolu

**Symptôme :** `hostname -f` ne retourne pas le FQDN complet

**Solution :**
```bash
# Vérifier /etc/hosts
cat /etc/hosts

# S'assurer que la ligne suivante existe :
192.168.x.15    mail.formation.lan mail

# Recharger la configuration (redémarrage shell)
exec bash

# Vérifier à nouveau
hostname -f
```

---

### Problème 2 : DNS ne résout pas mail.formation.lan

**Symptôme :** `ping mail.formation.lan` échoue ou résout vers une mauvaise IP

**Diagnostic :**
```bash
# Vérifier le serveur DNS configuré
cat /etc/resolv.conf

# Doit contenir :
# nameserver 192.168.x.3
# search formation.lan
```

**Solution 1 : Vérifier la configuration Netplan**
```bash
sudo nano /etc/netplan/00-installer-config.yaml

# S'assurer que nameservers pointe vers vos DNS locaux
```

**Solution 2 : Vider le cache DNS**
```bash
sudo systemd-resolve --flush-caches
sudo systemctl restart systemd-resolved
```

**Solution 3 : Attendre la propagation DNS**
```bash
# La propagation DNS peut prendre 1-2 minutes
# Attendez et réessayez
sleep 60
ping -c 4 mail.formation.lan
```

---

### Problème 3 : Impossible de pinger formation.lan

**Symptôme :** `ping formation.lan` échoue

**Diagnostic :**
```bash
# Vérifier que le domaine apex est défini dans le DNS
nslookup formation.lan 192.168.x.3
```

**Solution :** Sur le serveur DNS primaire, vérifier que le domaine a un enregistrement A :
```bash
# Sur primaire.formation.lan
sudo nano /etc/bind/db.formation.lan

# S'assurer qu'il y a un enregistrement pour le domaine lui-même :
@       IN      A       192.168.x.3
# ou pointer vers une machine spécifique
```

---

### Problème 4 : Erreur "Temporary failure in name resolution"

**Symptôme :** Les commandes réseau échouent avec cette erreur

**Solution :**
```bash
# Vérifier que systemd-resolved fonctionne
sudo systemctl status systemd-resolved

# Redémarrer si nécessaire
sudo systemctl restart systemd-resolved

# Vérifier /etc/resolv.conf
cat /etc/resolv.conf
```

---

## 7. Checklist de validation avant installation iRedMail

Cochez chaque élément avant de procéder à l'installation d'iRedMail :

- [ ] La VM `MAIL-US24` est créée et démarrée
- [ ] L'adresse IP statique `192.168.x.15` est configurée
- [ ] La passerelle réseau est accessible (`ping 192.168.x.1`)
- [ ] Le serveur DNS est accessible (`ping 192.168.x.3`)
- [ ] Le hostname est défini à `mail` (`hostname`)
- [ ] Le FQDN retourne `mail.formation.lan` (`hostname -f`)
- [ ] Le fichier `/etc/hosts` est correctement configuré
- [ ] `ping mail.formation.lan` fonctionne
- [ ] `nslookup mail.formation.lan` retourne `192.168.x.15`
- [ ] `ping formation.lan` fonctionne
- [ ] Les autres machines du domaine sont accessibles
- [ ] La connexion Internet fonctionne (si applicable)

---

## 8. Commandes de vérification rapide (tout-en-un)

**Script de vérification complète :**

```bash
#!/bin/bash
echo "=== Vérification de la configuration de base ==="
echo ""

echo "1. Hostname :"
hostname
hostname -f
echo ""

echo "2. Adresse IP :"
ip addr show | grep "inet " | grep -v "127.0.0.1"
echo ""

echo "3. Passerelle :"
ip route | grep default
echo ""

echo "4. Serveurs DNS :"
cat /etc/resolv.conf | grep nameserver
echo ""

echo "5. Fichier /etc/hosts :"
cat /etc/hosts | grep -v "^#"
echo ""

echo "6. Test de résolution DNS :"
nslookup mail.formation.lan
echo ""

echo "7. Test de connectivité :"
ping -c 2 mail.formation.lan
echo ""

echo "=== Fin de la vérification ==="
```

**Copier ce script, le sauvegarder dans `check-config.sh` et l'exécuter :**
```bash
bash check-config.sh
```

---

## 9. Prochaine étape

Une fois **toutes les vérifications passées**, vous êtes prêt à procéder à l'installation d'iRedMail.

➡️ **Passez au document : "Installation d'iRedMail sur Ubuntu Server 24.04 LTS"**

---

## 10. Notes importantes

### Patience avec la propagation DNS

⏱️ **La propagation DNS peut prendre du temps** :
- En environnement local : 10 secondes à 2 minutes
- Cache DNS des machines : jusqu'à 5 minutes
- Si ça ne fonctionne pas immédiatement, **attendez 2-3 minutes** et réessayez

### Importance du FQDN

Le **FQDN (Fully Qualified Domain Name)** est critique pour iRedMail :
- ❌ `mail` seul ne suffit pas
- ✅ `mail.formation.lan` est requis
- Le FQDN doit contenir **au moins un point**
- Le FQDN doit être **résolvable** par DNS

### Environnement de formation vs Production

| Aspect | Formation (formation.lan) | Production (exemple.com) |
|--------|---------------------------|--------------------------|
| Domaine | `.lan` (privé) | `.com`, `.ca` (public) |
| DNS | Serveur BIND local | DNS publics (Cloudflare, etc.) |
| IP | 192.168.x.x (privée) | IP publique |
| Emails externes | ❌ Impossible | ✅ Possible |
| Emails internes | ✅ Fonctionne | ✅ Fonctionne |

**Pour la formation**, le domaine `.lan` est parfait car il permet d'apprendre tous les concepts sans frais ni exposition publique.

---

## Résumé des étapes

1. ✅ Configurer le DNS avec l'enregistrement A pour `mail.formation.lan`
2. ✅ Créer la VM `MAIL-US24` dans Proxmox
3. ✅ Configurer l'IP statique `192.168.x.15`
4. ✅ Définir le hostname à `mail`
5. ✅ Corriger le fichier `/etc/hosts`
6. ✅ Valider la résolution DNS et la connectivité
7. ✅ Patienter pour la propagation DNS
8. ➡️ Procéder à l'installation d'iRedMail

**Vous êtes maintenant prêt pour l'installation du serveur mail !** 🚀