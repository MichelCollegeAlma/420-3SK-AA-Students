## 1. Installation et Configuration de Pi-hole sur Ubuntu 24

Ce guide décrit l'installation complète de Pi-hole sur un serveur Ubuntu 24 en machine virtuelle pour servir de serveur DNS pour le domaine `formation.lan`.

### 1.1 Prérequis

**Configuration du serveur :**
- Système d'exploitation : Ubuntu Server 24.04 LTS
- Adresse IP statique : `192.168.100.5` (où 100 est votre sous-réseau)
- Nom d'hôte : `pihole.formation.lan`
- RAM minimale : 512 MB (recommandé : 1 GB)
- Espace disque : 4 GB minimum

### 1.2 Configuration de l'adresse IP statique

Avant l'installation de Pi-hole, configurez une adresse IP statique.

**Éditer la configuration réseau avec Netplan :**

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

**Configuration à appliquer :**

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:  # Adapter selon votre interface (utilisez 'ip a' pour vérifier)
      dhcp4: no
      addresses:
        - 192.168.100.5/24
      routes:
        - to: default
          via: 192.168.100.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

**Appliquer la configuration :**

```bash
# Tester la configuration
sudo netplan try

# Si tout fonctionne, appliquer définitivement
sudo netplan apply

# Vérifier l'adresse IP
ip addr show
```

### 1.3 Configuration du nom d'hôte

```bash
# Définir le nom d'hôte
sudo hostnamectl set-hostname pihole

# Éditer /etc/hosts
sudo nano /etc/hosts
```

**Contenu de /etc/hosts :**

```
127.0.0.1       localhost
192.168.100.5   pihole.formation.lan pihole

# Les lignes suivantes sont souhaitables pour les hôtes compatibles IPv6
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

### 1.4 Mise à jour du système

```bash
# Mettre à jour les paquets
sudo apt update && sudo apt upgrade -y

# Installer les outils nécessaires
sudo apt install curl wget git -y
```

### 1.5 Installation de Pi-hole

**Télécharger et exécuter le script d'installation :**

```bash
# Télécharger le script d'installation automatique
curl -sSL https://install.pi-hole.net | bash
```

**Pendant l'installation, vous serez guidé par un assistant interactif :**

1. **Écran de bienvenue** : Appuyez sur `Enter`

2. **Donation notice** : Appuyez sur `Enter`

3. **Interface réseau** : Sélectionnez votre interface (généralement `ens33` ou `eth0`)

4. **Upstream DNS Provider** : Choisissez un fournisseur DNS temporaire
   - Google (recommandé pour l'installation)
   - Nous le configurerons manuellement après

5. **Blocklists** : Laissez les listes par défaut cochées

6. **Protocoles** : 
   - IPv4 : `Yes`
   - IPv6 : `Yes` (ou `No` si vous n'utilisez pas IPv6)

7. **Adresse IP statique** :
   - Confirmez l'adresse IP : `192.168.100.5/24`
   - Gateway : `192.168.100.1`

8. **Interface Web** : `Yes` (installation de l'interface d'administration)

9. **Serveur Web** : `Yes` (installation de lighttpd)

10. **Mode d'enregistrement** : 
    - `Show everything` (pour le développement)
    - Vous pourrez le changer plus tard

11. **Privacy mode** : Choisissez selon vos besoins (recommandé : `Show everything` pour les tests)

**À la fin de l'installation, notez :**
- L'adresse de l'interface web : `http://192.168.100.5/admin`
- Le mot de passe administrateur généré automatiquement

### 1.6 Configuration post-installation

**⚠️ IMPORTANT : Configurer le mot de passe administrateur**

Avant toute chose, définissez un mot de passe sécurisé pour l'interface web de Pi-hole.

```bash
# Définir un nouveau mot de passe administrateur
pihole setpassword
```

**Critères de sécurité recommandés pour le mot de passe :**
- Minimum 12 caractères
- Combinaison de majuscules et minuscules
- Au moins un chiffre
- Au moins un caractère spécial (!@#$%^&*)
- Éviter les mots du dictionnaire

**Exemple de mot de passe sécurisé :** `P!h0le#2024$Secur`

**🔒 NOTEZ CE MOT DE PASSE** dans un gestionnaire de mots de passe sécurisé ou dans un endroit sûr. Vous en aurez besoin pour accéder à l'interface web d'administration.

**Alternative - Utiliser la commande avec prompt :**

```bash
# Cette commande vous demandera d'entrer le mot de passe deux fois
pihole -a -p

# Entrez votre nouveau mot de passe lorsque demandé
# Ou laissez vide pour désactiver la connexion par mot de passe (NON RECOMMANDÉ)
```

**Vérifier le statut de Pi-hole :**

```bash
# Statut général
pihole status

# Version installée
pihole -v

# Statistiques
pihole -c
```

### 1.7 Configuration des enregistrements DNS locaux

**Via l'interface Web**

1. Accédez à l'interface web : `http://192.168.100.5/admin`

2. Connectez-vous avec votre mot de passe

3. Naviguez vers : **SYSTEM** → **Setting** → **Local DNS Records**

4. Ajoutez l'enregistrement pour le serveur mail :
   - **Domain** : `mail.formation.lan`
   - **Associated IP** : `192.168.100.15`
   - Cliquez sur **+**


### 1.10 Tests de résolution DNS

**Depuis une machine cliente (après avoir configuré le DNS sur 192.168.100.5) :**

**Test 1 : Résolution de l'enregistrement mail**

```bash
nslookup mail.formation.lan 192.168.100.5

# Résultat attendu :
# Server:         192.168.100.5
# Address:        192.168.100.5#53
#
# Name:   mail.formation.lan
# Address: 192.168.100.15
```

**Test 2 : Avec dig (plus détaillé)**

```bash
dig @192.168.100.5 mail.formation.lan

# Vérifier la section ANSWER :
# mail.formation.lan.      0       IN      A       192.168.100.15
```

**Test 3 : Depuis le serveur Pi-hole lui-même**

```bash
# Test local
dig mail.formation.lan

# Test de tous les enregistrements
dig formation.lan ANY
```

**Test 4 : Vérifier le blocage de publicités**

```bash
# Tester un domaine de publicité connu
nslookup doubleclick.net 192.168.100.5

# Devrait retourner 0.0.0.0 ou l'IP de Pi-hole
```

### 1.11 Configuration des clients pour utiliser Pi-hole

**Option 1 : Configuration manuelle sur chaque client**

Configurez les paramètres réseau pour utiliser `192.168.100.5` comme serveur DNS.

**Option 2 : Configuration via DHCP (Recommandé)**

Sur votre serveur DHCP, configurez :
- **DNS primaire** : `192.168.100.5`
- **Nom de domaine** : `formation.lan`

### 1.12 Commandes utiles de Pi-hole

```bash
# Afficher le statut
pihole status

# Désactiver Pi-hole temporairement (30 secondes)
pihole disable 30s

# Réactiver Pi-hole
pihole enable

# Mettre à jour Pi-hole
pihole -up

# Mise à jour de Gravity (listes de blocage)
pihole -g

# Voir les logs en temps réel
pihole -t

# Statistiques détaillées
pihole -c

# Whitelist un domaine
pihole -w example.com

# Blacklist un domaine
pihole -b ads.example.com

# Redémarrer le service DNS
pihole restartdns

# Voir la version
pihole -v
```
### 1.13 Dépannage

**Pi-hole ne démarre pas :**

```bash
# Vérifier les logs
sudo journalctl -u pihole-FTL -n 50

# Vérifier la configuration
pihole -d
```

**Les DNS locaux ne fonctionnent pas :**

```bash
# Vérifier le fichier custom.list
cat /etc/pihole/custom.list

# Forcer le rechargement
sudo pihole restartdns reload-lists

# Vider le cache DNS
sudo pihole restartdns flush-cache
```

**L'interface web n'est pas accessible :**

```bash
# Vérifier lighttpd
sudo systemctl status lighttpd

# Redémarrer lighttpd
sudo systemctl restart lighttpd

# Réparer l'installation
pihole -r
```

### 1.6 Vérification finale

✅ **Liste de contrôle avant de continuer :**

- [ ] Pi-hole est installé et fonctionnel
- [ ] L'adresse IP statique est configurée (192.168.100.5)
- [ ] L'interface web est accessible
- [ ] L'enregistrement DNS `mail.formation.lan → 192.168.100.15` est configuré
- [ ] La résolution DNS fonctionne depuis les clients
- [ ] Le blocage des publicités est actif

**Vous êtes maintenant prêt à installer et configurer votre serveur mail !**

---

## Notes supplémentaires

### Différences entre Pi-hole et BIND9

Pi-hole est basé sur **dnsmasq** et offre :
- ✅ Interface web intuitive
- ✅ Blocage de publicités intégré
- ✅ Statistiques détaillées
- ✅ Configuration simple
- ✅ Faible consommation de ressources

Pour un serveur DNS d'entreprise avec des besoins avancés (zones secondaires, DNSSEC, transferts de zone), BIND9 reste plus approprié.

### Logs et monitoring

- **Interface web** : Dashboard avec statistiques en temps réel
- **Logs FTL** : `/var/log/pihole/FTL.log`
- **Logs dnsmasq** : `/var/log/pihole/pihole.log`
- **Requêtes en temps réel** : Disponibles dans l'interface web sous **Query Log**
