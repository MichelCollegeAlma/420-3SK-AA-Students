# 4/5 - Installation d’un deuxième site Apache pour `forum.deepweb.com`

## Hypothèses
- Serveur Ubuntu 24 déjà installé avec Apache fonctionnel.
- Le premier site `deepweb.com` existe déjà dans `/var/www/html/deepweb.com`.
- Adresse IP du serveur : `192.168.x.77` (à adapter selon le réseau).

---

## 1) Préparer le dossier du site

Créer un répertoire pour le nouveau site :
```bash
sudo mkdir -p /var/www/html/forum.deepweb.com
```

Créer le fichier `index.html` :
```bash
echo "Forum PhpBB3 TEST" | sudo tee /var/www/html/forum.deepweb.com/index.html
```

Donner les bons droits :
```bash
sudo chown -R www-data:www-data /var/www/html/forum.deepweb.com
sudo chmod -R 755 /var/www/html/forum.deepweb.com
```

---

## 2) Configurer Apache pour `forum.deepweb.com`

Créer le fichier de configuration :
```bash
sudo tee /etc/apache2/sites-available/forum.deepweb.com.conf > /dev/null <<'EOF'
<VirtualHost *:80>
    ServerName forum.deepweb.com
    DocumentRoot /var/www/html/forum.deepweb.com

    <Directory /var/www/html/forum.deepweb.com>
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/forum.deepweb.com_error.log
    CustomLog ${APACHE_LOG_DIR}/forum.deepweb.com_access.log combined
</VirtualHost>
EOF
```

Activer le site et recharger Apache :
```bash
sudo a2ensite forum.deepweb.com.conf
sudo systemctl reload apache2
```

---

## 3) Configuration de l’hôte Windows pour accéder à `forum.deepweb.com`

1. Ouvrir Bloc-notes en mode administrateur.  
2. Éditer le fichier :
```
C:\Windows\System32\drivers\etc\hosts
```
3. Ajouter la ligne suivante (adapter l’IP) :
```
192.168.x.77   forum.deepweb.com
```
4. Sauvegarder et vider le cache DNS si nécessaire :
```powershell
ipconfig /flushdns
```

5. Tester depuis Windows :
```cmd
ping forum.deepweb.com
curl http://forum.deepweb.com
```
Ou ouvrir `http://forum.deepweb.com` dans un navigateur : la page doit afficher **Forum PhpBB3 TEST**.

---

## Résultat attendu
- Apache sert le site `forum.deepweb.com` avec le fichier `index.html`.  
- Depuis un poste Windows, accéder à `http://forum.deepweb.com` affiche le texte *Forum PhpBB3 TEST*.
