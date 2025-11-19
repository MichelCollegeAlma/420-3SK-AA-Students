# Liste des commandes utilisées pour la configuration du serveur LAMP

Ce document récapitule les principales commandes utilisées lors de la configuration du serveur LAMP, avec leur description et un exemple d’utilisation.

---

## 1) Gestion du système et réseau

### `ip a`
- **Description** : Affiche la configuration des interfaces réseau (IP, MAC, état).  
- **Exemple** :
```bash
ip a
```

### `ping`
- **Description** : Teste la connectivité réseau avec une autre machine.  
- **Exemple** :
```bash
ping 192.168.x.77
```

### `ssh`
- **Description** : Permet de se connecter en ligne de commande à une machine distante.  
- **Exemple** :
```bash
ssh test@192.168.x.77
```

### `sudo netplan apply`
- **Description** : Applique la configuration réseau définie dans les fichiers `/etc/netplan/`.  
- **Exemple** :
```bash
sudo netplan apply
```

---

## 2) Gestion des paquets et logiciels

### `sudo apt update && sudo apt upgrade -y`
- **Description** : Met à jour la liste des paquets et applique les mises à jour disponibles.  
- **Exemple** :
```bash
sudo apt update && sudo apt upgrade -y
```

### `sudo apt install <package>`
- **Description** : Installe un logiciel ou un paquet.  
- **Exemple** :
```bash
sudo apt install apache2 mysql-server php libapache2-mod-php unzip -y
```

---

## 3) Commandes liées à Apache

### `sudo systemctl reload apache2`
- **Description** : Recharge la configuration d’Apache sans arrêter le service.  
- **Exemple** :
```bash
sudo systemctl reload apache2
```

### `sudo systemctl restart apache2`
- **Description** : Redémarre complètement le service Apache.  
- **Exemple** :
```bash
sudo systemctl restart apache2
```

### `sudo a2enmod rewrite`
- **Description** : Active le module `mod_rewrite` d’Apache (utile pour WordPress).  
- **Exemple** :
```bash
sudo a2enmod rewrite
```

### `sudo a2ensite <site>.conf`
- **Description** : Active un site Apache configuré dans `/etc/apache2/sites-available/`.  
- **Exemple** :
```bash
sudo a2ensite deepweb.com.conf
```

### `sudo a2dissite <site>.conf`
- **Description** : Désactive un site Apache.  
- **Exemple** :
```bash
sudo a2dissite 000-default.conf
```

### `sudo tee /etc/apache2/sites-available/<site>.conf`
- **Description** : Crée un fichier de configuration Apache via redirection de contenu.  
- **Exemple** :
```bash
sudo tee /etc/apache2/sites-available/deepweb.com.conf > /dev/null <<'EOF'
<VirtualHost *:80>
    ServerName deepweb.com
    DocumentRoot /var/www/html/deepweb.com
</VirtualHost>
EOF
```

---

## 4) Commandes liées aux fichiers et permissions

### `sudo mkdir -p <dossier>`
- **Description** : Crée un dossier, avec option `-p` pour créer l’arborescence complète.  
- **Exemple** :
```bash
sudo mkdir -p /var/www/html/deepweb.com
```

### `sudo chown -R <user>:<group> <dossier>`
- **Description** : Change le propriétaire et le groupe d’un dossier et de son contenu.  
- **Exemple** :
```bash
sudo chown -R www-data:www-data /var/www/html/deepweb.com
```

### `sudo chmod -R 755 <dossier>`
- **Description** : Définit les permissions en lecture/exécution pour tous, écriture pour le propriétaire.  
- **Exemple** :
```bash
sudo chmod -R 755 /var/www/html/deepweb.com
```

### `echo "texte" | sudo tee <fichier>`
- **Description** : Écrit du texte directement dans un fichier (utile pour un `index.html`).  
- **Exemple** :
```bash
echo "Forum PhpBB3 TEST" | sudo tee /var/www/html/forum.deepweb.com/index.html
```

---

## 5) Commandes liées au téléchargement et extraction

### `curl -O <url>`
- **Description** : Télécharge un fichier depuis une URL (option `-O` garde le nom original).  
- **Exemple** :
```bash
curl -O https://fr.wordpress.org/latest-fr_FR.tar.gz
```

### `wget <url>`
- **Description** : Télécharge un fichier depuis une URL (équivalent de `curl -O`).  
- **Exemple** :
```bash
wget https://download.phpbb.com/pub/release/3.3/3.3.11/phpBB-3.3.11.zip
```

### `tar xzf <archive>`
- **Description** : Décompresse une archive tar.gz.  
- **Exemple** :
```bash
tar xzf latest-fr_FR.tar.gz
```

### `unzip <archive>`
- **Description** : Décompresse une archive ZIP.  
- **Exemple** :
```bash
unzip phpBB-3.3.11.zip
```

### `cp -R <source> <destination>`
- **Description** : Copie récursive d’un dossier.  
- **Exemple** :
```bash
sudo cp -R wordpress/* /var/www/html/deepweb.com/
```

---

## 6) Commandes liées à MySQL

### `sudo mysql -u root -p`
- **Description** : Connexion au serveur MySQL en tant qu’administrateur root.  
- **Exemple** :
```bash
sudo mysql -u root -p
```

### `GRANT ALL PRIVILEGES`
- **Description** : Donne tous les privilèges à un utilisateur sur une base donnée.  
- **Exemple** :
```sql
GRANT ALL PRIVILEGES ON deepweb.com.* TO 'deepweb.com'@'localhost' IDENTIFIED BY 'test';
FLUSH PRIVILEGES;
```

---

## 7) Commandes de diagnostic

### `sudo tail -n 100 /var/log/apache2/<fichier>.log`
- **Description** : Affiche les 100 dernières lignes d’un log Apache (erreurs ou accès).  
- **Exemple** :
```bash
sudo tail -n 100 /var/log/apache2/deepweb.com_error.log
```

### `ipconfig /flushdns` (Windows)
- **Description** : Vide le cache DNS sous Windows.  
- **Exemple** :
```powershell
ipconfig /flushdns
```

### `curl http://<site>`
- **Description** : Vérifie la réponse HTTP d’un site en ligne de commande.  
- **Exemple** :
```bash
curl http://deepweb.com
```

---

---

## 8) Commandes liées au DNS (Bind9)

### `sudo apt install bind9 bind9utils net-tools -y`
- **Description** : Installe le serveur DNS Bind9 et ses utilitaires.  
- **Exemple** :
```bash
sudo apt install bind9 bind9utils net-tools -y
```

### `sudo systemctl restart bind9`
- **Description** : Redémarre le service Bind9.  
- **Exemple** :
```bash
sudo systemctl restart bind9
```

### `sudo systemctl status bind9`
- **Description** : Vérifie l’état du service Bind9.  
- **Exemple** :
```bash
sudo systemctl status bind9
```

### `named-checkconf`
- **Description** : Vérifie la syntaxe des fichiers de configuration BIND.  
- **Exemple** :
```bash
named-checkconf
```

### `named-checkconf -z`
- **Description** : Vérifie la configuration complète, y compris les zones déclarées.  
- **Exemple** :
```bash
named-checkconf -z
```

### `named-checkzone <zone> <fichier>`
- **Description** : Vérifie la cohérence syntaxique d’un fichier de zone.  
- **Exemple** :
```bash
named-checkzone formation.lan /etc/bind/db.formation.lan
```

### `dig <nom>`
- **Description** : Interroge le serveur DNS pour une résolution de nom.  
- **Exemple** :
```bash
dig host1.formation.lan
```

### `dig -x <IP>`
- **Description** : Effectue une recherche inverse (IP → nom).  
- **Exemple** :
```bash
dig -x 192.168.100.11
```

### `nslookup <nom>`
- **Description** : Interroge le DNS pour résoudre un nom.  
- **Exemple** :
```bash
nslookup host1.formation.lan
```

### `nslookup <IP>`
- **Description** : Recherche inverse sur une IP donnée.  
- **Exemple** :
```bash
nslookup 192.168.100.11
```

### `resolvectl status`
- **Description** : Vérifie les serveurs DNS utilisés par systemd-resolved.  
- **Exemple** :
```bash
resolvectl status
```

### `ipconfig /all` (Windows)
- **Description** : Affiche la configuration réseau, y compris les serveurs DNS configurés.  
- **Exemple** :
```powershell
ipconfig /all
```
