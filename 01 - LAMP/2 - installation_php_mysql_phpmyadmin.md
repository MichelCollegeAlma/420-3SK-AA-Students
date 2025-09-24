# 2/5 - Installation de PHP, MySQL et phpMyAdmin sur Ubuntu 24 Server

## Mise à jour du système

``` bash
sudo apt update && sudo apt upgrade -y
```

## Installation de PHP

``` bash
sudo apt install php libapache2-mod-php php-mysql -y
```

Vérification de la version :

``` bash
php -v
```

### Test d'accès au service HTTP depuis un poste Windows

Ouvrir un navigateur web (Edge, Chrome, Firefox) et saisir :

    http://<IP_SERVEUR>

La page par défaut d'Apache ("It works!") doit s'afficher.
![img.png](img/itworks.png)
## Installation de MySQL

``` bash
sudo apt install mysql-server -y
```

Sécurisation de l'installation :

``` bash
sudo mysql_secure_installation
```
TRÈS IMPORTANT DE SUIVRE LES INDICATIONS SINON VOUS DEVREZ EFFACER, PURGER ET RECOMMENCER.
- Would you like to setup VALIDATE PASSWORD component?    : **NO**
- Remove anonymous users?    : No
- Disallow root login remotely?    : No
- Remove test database and access to it?    : No
- Reload privilege tables now? : **YES**

Connexion au shell MySQL :

``` bash
sudo mysql -u root -p
```
Quitter shell MySQL :

``` bash
quit
```

## Installation de phpMyAdmin

``` bash
sudo apt install phpmyadmin php-mbstring php-zip php-gd php-json php-curl -y
```
- Fenêtre installation
  - Espace pour sélectionner "apache2"
  - Tab pour sélectionner "Ok" et Enter
- Fenêtre "Configuring phpmyadmin"
  - Enter pour sélectionner "Yes"
  - Password for phpmyadmin: test

Activer les extensions PHP nécessaires :

``` bash
sudo phpenmod mbstring
sudo systemctl restart apache2
```

## Configuration d'Apache pour phpMyAdmin

Un lien symbolique peut être créé si nécessaire :

``` bash
sudo ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin
```

### Donner les droits administrateur à l’utilisateur phpMyAdmin

#### Étape 1 : Connexion à MySQL en root
```bash
sudo mysql -u root -p
```

#### Étape 2 : Accorder les privilèges à l’utilisateur `phpmyadmin`
```sql
GRANT ALL PRIVILEGES ON *.* TO 'phpmyadmin'@'localhost' WITH GRANT OPTION;
```

#### Étape 3 : Recharger les privilèges
```sql
FLUSH PRIVILEGES;
```

#### Étape 4 : Vérifier les privilèges
```sql
SHOW GRANTS FOR 'phpmyadmin'@'localhost';
```

#### Remarque
Cette opération donne un accès complet à l’utilisateur `phpmyadmin`.  
En production, il est recommandé de créer un compte administrateur distinct et de limiter les droits de `phpmyadmin`.


## Accès à phpMyAdmin

Ouvrir dans le navigateur :

    http://<IP_SERVEUR>/phpmyadmin

Se connecter avec l'utilisateur et le mot de passe MySQL.
- Utiliseur: phpmyadmin
- Mot de passe: test 
