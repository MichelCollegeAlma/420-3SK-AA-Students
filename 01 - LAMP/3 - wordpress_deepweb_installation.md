# 3/5 - Installation de WordPress sur Ubuntu 24 pour le domaine `deepweb.com`

## Hypothèses
- Serveur Ubuntu 24 installé et accessible sur le LAN.
- Apache, PHP et MySQL installés. phpMyAdmin disponible et fonctionnel.
- Adresse IP du serveur : `192.168.x.77` (remplacer par l'IP réelle).
- Dossier web : `/var/www/html/deepweb.com/`.
- Nom d'utilisateur MySQL à créer via phpMyAdmin : `deepweb.com` (mot de passe : `test`).
- Une base du même nom `deepweb.com` sera créée via phpMyAdmin et l'utilisateur recevra tous les privilèges sur cette base.

---

## 1) Créer l’utilisateur MySQL et la base via phpMyAdmin (interface graphique uniquement)

1. Ouvrir phpMyAdmin : `http://<IP_SERVEUR>/phpmyadmin`  
2. Aller dans l'onglet **"Utilisateurs"**.  
3. Cliquer sur **"Ajouter un utilisateur"**.  
   - Nom d'utilisateur : `deepweb.com`  
   - Hôte : `localhost`  
   - Mot de passe : `test`  
4. Cocher **"Créer une base du même nom et accorder tous les privilèges"** si disponible.  
   - Si phpMyAdmin propose la création automatique de la base, laisser cette option activée.  
5. Ensuite, via **Utilisateurs → Modifier les privilèges** pour `deepweb.com`, vérifier que tous les privilèges sont cochés pour la base `deepweb.com`.  
6. Vérifier que les privilèges incluent la gestion des données et de la structure (SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, etc.).

---

## 2) Préparer Apache et le dossier web

1. Créer le répertoire web et appliquer les permissions de base :
```bash
sudo mkdir -p /var/www/html/deepweb.com
sudo chown -R $USER:$USER /var/www/html/deepweb.com
sudo chmod -R 750 /var/www/html/deepweb.com
```

2. Télécharger WordPress et copier les fichiers :
```bash
cd /tmp
curl -O https://fr.wordpress.org/latest-fr_FR.tar.gz
tar xzf latest-fr_FR.tar.gz
sudo cp -R wordpress/* /var/www/html/deepweb.com/
```

3. Ajuster propriétaires et permissions pour Apache :
```bash
sudo chown -R www-data:www-data /var/www/html/deepweb.com
sudo find /var/www/html/deepweb.com -type d -exec chmod 755 {} \;
sudo find /var/www/html/deepweb.com -type f -exec chmod 644 {} \;
```
À partir d'ici votre site est accessible à l'adresse

    http://<IP_SERVEUR>/deepweb.com

Testez-le, mais ne faites pas l'installation.

4. Créer le fichier de configuration Apache :
```bash
sudo tee /etc/apache2/sites-available/deepweb.com.conf > /dev/null <<'EOF'
<VirtualHost *:80>
    ServerName deepweb.com
    ServerAlias www.deepweb.com
    DocumentRoot /var/www/html/deepweb.com

    <Directory /var/www/html/deepweb.com>
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/deepweb.com_error.log
    CustomLog ${APACHE_LOG_DIR}/deepweb.com_access.log combined
</VirtualHost>
EOF
```

5. Activer le site et modules, recharger Apache :
```bash
sudo a2enmod rewrite
sudo a2ensite deepweb.com.conf
sudo systemctl reload apache2
```

---

## 3) Configurer WordPress (`wp-config.php`)

1. Copier le fichier d'exemple et éditer :
```bash
cd /var/www/html/deepweb.com
sudo cp wp-config-sample.php wp-config.php
sudo nano wp-config.php
```

2. Modifier les paramètres de la base de données :
```php
/** Nom de la base de données de WordPress */
define('DB_NAME', 'deepweb.com');

/** Nom d'utilisateur MySQL */
define('DB_USER', 'deepweb.com');

/** Mot de passe MySQL */
define('DB_PASSWORD', 'test');

/** Adresse de l'hébergement MySQL */
define('DB_HOST', 'localhost');

/** Jeu de caractères à utiliser pour la création des tables. */
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');
```

3. Remplacer les clés de sécurité par des valeurs générées :
- Aller sur https://api.wordpress.org/secret-key/1.1/salt/  
- Copier les clés et remplacer les constantes correspondantes dans `wp-config.php`.

4. Vérifier propriétaires :
```bash
sudo chown -R www-data:www-data /var/www/html/deepweb.com
```

---

## 4) Configuration de l’hôte Windows pour accéder à `deepweb.com`

1. Ouvrir Bloc-notes en mode administrateur.  
2. Ouvrir le fichier :
```
C:\Windows\System32\drivers\etc\hosts
```
3. Ajouter la ligne suivante, remplacer `192.168.x.77` si nécessaire :
```
192.168.x.77   deepweb.com www.deepweb.com
```
4. Sauvegarder. Vider le cache DNS si besoin :
```powershell
ipconfig /flushdns
```
5. Tester depuis Windows :
```cmd
ping deepweb.com
curl http://deepweb.com
```
Ou ouvrir `http://deepweb.com` dans un navigateur.

* si ça ne fonctionne pas, utilisez la navigation privée.

---

## 5) Finaliser l’installation WordPress via l’interface web

1. Ouvrir `http://deepweb.com` depuis le poste Windows.  
2. Suivre l’assistant d’installation WordPress :
   - Choisir la langue.
   - Saisir le titre du site: Deep Web
   - Identifiant: `admin`
   - Mot de passe: `test`
   - E-mail: `admin@deepweb.com`
3. Valider dans PhpMyAdmin. WordPress créera les tables dans la base `deepweb.com` à condition que l’utilisateur MySQL `deepweb.com` ait les privilèges nécessaires.

---

## 6) Vérifications rapides
- Vérifier que la page d’accueil WordPress s’affiche.  
- Vérifier dans phpMyAdmin la présence des tables dans la base `deepweb.com`.  
- Consulter les logs Apache si erreur :
```bash
sudo tail -n 100 /var/log/apache2/deepweb.com_error.log
```

---

## 5) Accès à l'administration et test final

1. Ouvrir `http://deepweb.com/wp-admin` depuis le poste Windows.
2. Connectez-vous  
   - Identifiant: `admin`
   - Mot de passe: `test`
3. Dans `Médias`, tentez de téléverser une image.
   - Si ça ne fonctionne pas, faites les corrections nécessaires. (Vous devrez faires quelques recherches.)
4. Naviguez dans l'interface et ajoutez du contenu au blogue.


---

## 7) Remarques de sécurité
- Remplacer le mot de passe `test` immédiatement en production.  
- Restreindre l’accès à phpMyAdmin en production.  
- Utiliser TLS pour un site public.
