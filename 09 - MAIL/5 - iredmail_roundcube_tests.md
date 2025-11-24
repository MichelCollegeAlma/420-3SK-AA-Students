# Exercice pratique iRedMail
## Tests complets des fonctionnalités Roundcube et iRedAdmin

---

## Objectifs de l'exercice

À la fin de cet exercice, vous serez capable de :
1. Créer et gérer des comptes utilisateurs via iRedAdmin
2. Utiliser toutes les fonctionnalités de Roundcube (webmail)
3. Tester l'envoi et la réception d'emails
4. Gérer les dossiers, contacts et paramètres utilisateur
5. Monitorer toutes les opérations via les logs en temps réel
6. Valider le bon fonctionnement de l'ensemble du système mail

---

## Prérequis

- Serveur iRedMail installé et tous les services démarrés
- Accès à iRedAdmin : https://mail.formation.lan/iredadmin
- Accès à Roundcube : https://mail.formation.lan/mail
- 2 terminaux SSH ouverts sur le serveur

---

## Matériel nécessaire

- **Terminal 1** : Monitoring des logs en temps réel
- **Terminal 2** : Commandes de diagnostic et vérification
- **Navigateur 1** : iRedAdmin (gestion administrateur)
- **Navigateur 2** : Roundcube (interface utilisateur)

💡 **Astuce** : Utilisez deux fenêtres de navigateur côte à côte ou deux navigateurs différents

---

## Préparation de l'environnement

### Étape 0.1 : Démarrer le monitoring

**Terminal 1 - Surveillance continue des logs**
```bash
ssh test@mail.formation.lan
sudo tail -f /var/log/mail.log
```

⚠️ **Important** : Gardez ce terminal visible pendant tout l'exercice

**Terminal 2 - Commandes de diagnostic**
```bash
ssh test@mail.formation.lan
```

### Étape 0.2 : Vérifier tous les services

Dans le **Terminal 2** :
```bash
echo "=== Vérification des services ==="
sudo systemctl is-active postfix dovecot nginx mariadb amavis clamav-daemon php8.3-fpm iredadmin iredapd
```

**Résultat attendu :** Tous les services doivent afficher `active`

Si un service est `inactive`, le démarrer :
```bash
sudo systemctl start nom_du_service
```

---

## PARTIE 1 : Gestion des utilisateurs (iRedAdmin)

### Exercice 1.1 : Créer trois comptes utilisateurs

**Objectif :** Créer 3 comptes email pour les tests

**Procédure :**

1. **Ouvrir iRedAdmin**
   - URL : https://mail.formation.lan/iredadmin
   - Identifiants : `postmaster@formation.lan` / `test`

2. **Créer le premier utilisateur**
   - Cliquez sur **Domains** → **formation.lan** → **Users**
   - Cliquez sur **Add User**
   - Remplissez :
     - **Mail address** : `alice`
     - **Password** : `test123`
     - **Confirm password** : `test123`
     - **Display name** : `Alice Tremblay`
     - **Quota** : `1024` MB
   - Cliquez sur **Add**

3. **Observer les logs dans Terminal 1**
   - Vous devriez voir l'activité de création dans les logs

4. **Créer deux autres utilisateurs**
   
   **Utilisateur 2 :**
   - Mail : `bob@formation.lan`
   - Password : `test123`
   - Display name : `Bob Martin`
   - Quota : `1024` MB
   
   **Utilisateur 3 :**
   - Mail : `charlie@formation.lan`
   - Password : `test123`
   - Display name : `Charlie Gagnon`
   - Quota : `512` MB

5. **Vérifier dans Terminal 2**
```bash
sudo mysql -u root -ptest -e "USE vmail; SELECT username, name, quota FROM mailbox WHERE domain='formation.lan';"
```

**Tableau à remplir :**

| Utilisateur | Quota (MB) | Statut | Créé avec succès ? |
|-------------|------------|--------|-------------------|
| alice@formation.lan | 1024 | Active | ☐ Oui ☐ Non |
| bob@formation.lan | 1024 | Active | ☐ Oui ☐ Non |
| charlie@formation.lan | 512 | Active | ☐ Oui ☐ Non |

---

### Exercice 1.2 : Créer un alias email

**Objectif :** Créer un alias qui redirige vers plusieurs comptes

**Procédure :**

1. Dans iRedAdmin, cliquez sur **Domains** → **formation.lan** → **Aliases**
2. Cliquez sur **Add Alias**
3. Remplissez :
   - **Mail address** : `equipe`
   - **Display name** : `Équipe Formation`
   - **Redirect to** : `alice@formation.lan, bob@formation.lan`
4. Cliquez sur **Add**

**Test de validation :**
```bash
# Dans Terminal 2
sudo mysql -u root -ptest -e "USE vmail; SELECT address, goto FROM alias WHERE address='equipe@formation.lan';"
```

**Question :** Les deux adresses de destination apparaissent-elles ?
- ☐ Oui
- ☐ Non

---

### Exercice 1.3 : Modifier un quota utilisateur

**Objectif :** Augmenter le quota de Charlie

**Procédure :**

1. Dans iRedAdmin, allez dans **Users**
2. Cliquez sur `charlie@formation.lan`
3. Modifiez **Quota** de `512` à `2048` MB
4. Cliquez sur **Update**

**Validation dans Terminal 2 :**
```bash
sudo mysql -u root -ptest -e "USE vmail; SELECT username, quota FROM mailbox WHERE username='charlie@formation.lan';"
```

**Question :** Le quota affiché est-il maintenant 2147483648 (2048 MB en bytes) ?
- ☐ Oui
- ☐ Non

---

## PARTIE 2 : Tests de Roundcube - Utilisateur Alice

### Exercice 2.1 : Première connexion

**Procédure :**

1. **Ouvrir Roundcube dans un nouvel onglet/fenêtre**
   - URL : https://mail.formation.lan/mail

2. **Se connecter avec Alice**
   - **Username** : `alice@formation.lan`
   - **Password** : `test123`
   - Cliquez sur **Login**

3. **Observer les logs dans Terminal 1**

**Logs attendus :**
```
dovecot: imap-login: Login: user=<alice@formation.lan>
```

**Question :** Voyez-vous la connexion d'Alice dans les logs ?
- ☐ Oui
- ☐ Non

4. **Explorer l'interface Roundcube**
   - Identifiez les sections : Inbox, Compose, Contacts, Settings

---

### Exercice 2.2 : Envoyer un email simple

**Objectif :** Envoyer un email de Alice vers Bob

**Procédure :**

1. **Composer l'email**
   - Cliquez sur **Compose** (icône crayon)
   - **To** : `bob@formation.lan`
   - **Subject** : `Test 1 - Premier email`
   - **Message** : 
     ```
     Bonjour Bob,
     
     Ceci est mon premier email de test.
     
     Cordialement,
     Alice
     ```
   - Cliquez sur **Send**

2. **Observer les logs dans Terminal 1**

**Logs attendus :**
```
postfix/submission/smtpd: connect from localhost[127.0.0.1]
postfix/submission/smtpd: client=localhost, sasl_method=LOGIN, sasl_username=alice@formation.lan
postfix/cleanup: message-id=<...>
roundcube: User alice@formation.lan; Message <...> for bob@formation.lan; 250: 2.0.0 Ok: queued
postfix/qmgr: from=<alice@formation.lan>, size=XXX, nrcpt=1 (queue active)
amavis: Passed CLEAN
postfix/smtp: to=<bob@formation.lan>, status=sent (delivered to mailbox)
```

**Checklist d'observation :**
- ☐ Connexion SMTP établie
- ☐ Authentification réussie (sasl_username=alice@formation.lan)
- ☐ Message accepté (250: 2.0.0 Ok: queued)
- ☐ Scan antivirus passé (Passed CLEAN)
- ☐ Livraison réussie (status=sent)

3. **Vérifier dans Terminal 2**
```bash
# Vérifier la file d'attente (doit être vide)
sudo postqueue -p
```

**Résultat attendu :** `Mail queue is empty`

---

### Exercice 2.3 : Envoyer un email avec copie carbone

**Objectif :** Envoyer un email à Bob avec Charlie en copie

**Procédure :**

1. Cliquez sur **Compose**
2. Remplissez :
   - **To** : `bob@formation.lan`
   - **Cc** : `charlie@formation.lan` (cliquez sur "Cc" pour afficher le champ)
   - **Subject** : `Test 2 - Email avec copie`
   - **Message** : `Email envoyé à Bob avec Charlie en copie`
3. Cliquez sur **Send**

**Observer Terminal 1 :**

**Question :** Combien de destinataires (nrcpt) sont mentionnés dans les logs ?
- Réponse : ________

**Attendu :** `nrcpt=2` (Bob + Charlie)

---

### Exercice 2.4 : Envoyer un email avec pièce jointe

**Objectif :** Tester l'envoi de fichiers et le scan antivirus

**Procédure :**

1. **Préparer un fichier test**
   - Créez un fichier texte simple sur votre ordinateur
   - Nom : `document-test.txt`
   - Contenu : `Ceci est un document de test pour validation`

2. **Composer l'email**
   - **To** : `bob@formation.lan`
   - **Subject** : `Test 3 - Pièce jointe`
   - **Message** : `Voir le document en pièce jointe`
   - Cliquez sur **Attach** (trombone) et sélectionnez votre fichier
   - Attendez que le fichier soit uploadé (barre de progression)
   - Cliquez sur **Send**

3. **Observer attentivement Terminal 1**

**Logs attendus - Phase d'analyse antivirus :**
```
amavis: FWD from <alice@formation.lan>
amavis: Checking: [EMAIL WITH ATTACHMENT]
amavis: p001 1 Content-Type: text/plain
amavis: Passed CLEAN
```

**Questions :**
1. Voyez-vous l'analyse de la pièce jointe par Amavis ? ☐ Oui ☐ Non
2. Le statut est-il "Passed CLEAN" ? ☐ Oui ☐ Non
3. La taille de l'email a-t-elle augmenté ? ☐ Oui ☐ Non

4. **Vérifier la taille dans Terminal 2**
```bash
# Voir les emails récents avec leur taille
sudo tail -50 /var/log/mail.log | grep "size="
```

---

### Exercice 2.5 : Utiliser l'alias équipe

**Objectif :** Vérifier que l'alias redirige correctement vers plusieurs destinataires

**Procédure :**

1. Composer un email :
   - **To** : `equipe@formation.lan`
   - **Subject** : `Test 4 - Alias équipe`
   - **Message** : `Message pour toute l'équipe`
2. Cliquez sur **Send**

3. **Observer Terminal 1**

**Logs attendus :**
```
postfix/cleanup: message-id=<...>
postfix/qmgr: from=<alice@formation.lan>, size=XXX, nrcpt=2 (queue active)
postfix/smtp: to=<alice@formation.lan>, relay=dovecot, status=sent
postfix/smtp: to=<bob@formation.lan>, relay=dovecot, status=sent
```

**Question :** Voyez-vous 2 destinataires (nrcpt=2) et 2 livraisons distinctes ?
- ☐ Oui
- ☐ Non

---

## PARTIE 3 : Réception et gestion des emails - Utilisateur Bob

### Exercice 3.1 : Se connecter avec Bob

**Procédure :**

1. **Déconnexion d'Alice**
   - Dans Roundcube, cliquez sur **Logout** (en haut à droite)

2. **Connexion avec Bob**
   - **Username** : `bob@formation.lan`
   - **Password** : `test123`
   - Cliquez sur **Login**

3. **Observer Terminal 1**
```
dovecot: imap-login: Login: user=<bob@formation.lan>
```

---

### Exercice 3.2 : Vérifier la réception des emails

**Procédure :**

1. **Vérifier la boîte de réception (Inbox)**
   - Vous devriez voir les 4 emails envoyés par Alice

2. **Compter les emails reçus**

**Tableau à remplir :**

| N° | Sujet | Expéditeur | Pièce jointe ? |
|----|-------|------------|----------------|
| 1 | Test 1 - Premier email | alice@formation.lan | ☐ Oui ☐ Non |
| 2 | Test 2 - Email avec copie | alice@formation.lan | ☐ Oui ☐ Non |
| 3 | Test 3 - Pièce jointe | alice@formation.lan | ☐ Oui ☐ Non |
| 4 | Test 4 - Alias équipe | alice@formation.lan | ☐ Oui ☐ Non |

**Question :** Avez-vous reçu tous les emails attendus ?
- ☐ Oui (4 emails)
- ☐ Non (précisez combien : ____)

---

### Exercice 3.3 : Lire et télécharger une pièce jointe

**Procédure :**

1. Cliquez sur l'email "Test 3 - Pièce jointe"
2. Vérifiez que la pièce jointe apparaît en bas de l'email
3. Cliquez sur l'icône de téléchargement
4. Ouvrez le fichier téléchargé

**Question :** Le contenu du fichier est-il identique à l'original ?
- ☐ Oui
- ☐ Non

---

### Exercice 3.4 : Répondre à un email

**Objectif :** Tester la fonction "Reply"

**Procédure :**

1. Ouvrez l'email "Test 1 - Premier email"
2. Cliquez sur **Reply** (Répondre)
3. Observez que :
   - Le champ **To** est automatiquement rempli avec `alice@formation.lan`
   - Le **Subject** commence par "Re: "
   - Le message original est cité
4. Ajoutez votre réponse :
   ```
   Bonjour Alice,
   
   J'ai bien reçu ton email de test.
   Tout fonctionne parfaitement !
   
   Bob
   ```
5. Cliquez sur **Send**

6. **Observer Terminal 1**

**Question :** Voyez-vous l'envoi de Bob vers Alice dans les logs ?
- ☐ Oui
- ☐ Non

---

### Exercice 3.5 : Transférer un email

**Objectif :** Tester la fonction "Forward"

**Procédure :**

1. Ouvrez l'email "Test 3 - Pièce jointe"
2. Cliquez sur **Forward** (Transférer)
3. Remplissez :
   - **To** : `charlie@formation.lan`
   - Ajoutez un message : `Charlie, regarde ce document`
4. Cliquez sur **Send**

**Observer Terminal 1 :**

**Questions :**
1. L'email est-il envoyé à Charlie ? ☐ Oui ☐ Non
2. La pièce jointe est-elle incluse dans le transfert ? (vérifier la taille) ☐ Oui ☐ Non

---

## PARTIE 4 : Gestion des dossiers

### Exercice 4.1 : Créer des dossiers personnalisés

**Objectif :** Organiser les emails dans des dossiers

**Procédure (toujours connecté avec Bob) :**

1. **Créer un dossier "Projets"**
   - Cliquez sur **Settings** (roue dentée) → **Folders**
   - En bas, dans le champ de texte, tapez : `Projets`
   - Cliquez sur **Create**

2. **Créer un dossier "Archives"**
   - Répétez avec le nom : `Archives`
   - Cliquez sur **Create**

3. **Vérifier dans l'interface**
   - Retournez dans **Mail**
   - Les nouveaux dossiers doivent apparaître dans la liste à gauche

**Validation dans Terminal 2 :**
```bash
# Lister les dossiers de Bob
sudo ls -la /var/vmail/vmail1/formation.lan/b/o/b/bob-*/Maildir/
```

**Question :** Voyez-vous les dossiers `.Projets` et `.Archives` ?
- ☐ Oui
- ☐ Non

---

### Exercice 4.2 : Déplacer des emails dans un dossier

**Procédure :**

1. Retournez dans **Inbox**
2. **Sélectionnez** l'email "Test 1 - Premier email" (cochez la case)
3. Cliquez sur **More** → **Move to** → **Projets**
4. L'email disparaît de la boîte de réception

5. **Vérifier le déplacement**
   - Cliquez sur le dossier **Projets** dans la liste de gauche
   - L'email doit s'y trouver

**Observer Terminal 1 :**
```
dovecot: imap: copy
dovecot: imap: expunge
```

---

### Exercice 4.3 : Marquer des emails

**Procédure :**

1. Dans **Inbox**, sélectionnez l'email "Test 2 - Email avec copie"
2. Cliquez sur l'**étoile** pour le marquer comme favori
3. L'étoile devient jaune/dorée

4. **Sélectionnez** l'email "Test 4 - Alias équipe"
5. Cliquez sur **More** → **Mark as** → **Unread** (marquer comme non lu)
6. L'email apparaît en gras

---

## PARTIE 5 : Gestion des contacts

### Exercice 5.1 : Ajouter des contacts

**Objectif :** Créer un carnet d'adresses

**Procédure :**

1. Cliquez sur **Contacts** (icône carnet)
2. Cliquez sur **Create** (bouton +)
3. Remplissez le formulaire :
   - **First name** : `Alice`
   - **Surname** : `Tremblay`
   - **Email** : `alice@formation.lan`
   - **Organization** : `Formation Inc.`
4. Cliquez sur **Save**

5. **Ajouter un second contact**
   - **First name** : `Charlie`
   - **Surname** : `Gagnon`
   - **Email** : `charlie@formation.lan`
   - Cliquez sur **Save**

**Question :** Les 2 contacts apparaissent-ils dans la liste ?
- ☐ Oui
- ☐ Non

---

### Exercice 5.2 : Utiliser un contact pour composer un email

**Procédure :**

1. Cliquez sur **Mail**
2. Cliquez sur **Compose**
3. Dans le champ **To**, commencez à taper : `Alice`
4. Une suggestion devrait apparaître : `Alice Tremblay <alice@formation.lan>`
5. Sélectionnez-la
6. **Annuler** l'email (bouton Cancel)

---

## PARTIE 6 : Paramètres utilisateur

### Exercice 6.1 : Changer la langue de l'interface

**Procédure :**

1. Cliquez sur **Settings** → **Preferences**
2. Section **User Interface**
3. **Language** : Sélectionnez `Français (France)`
4. Cliquez sur **Save**
5. L'interface se recharge en français

**Question :** L'interface est-elle maintenant en français ?
- ☐ Oui
- ☐ Non

---

### Exercice 6.2 : Configurer une signature email

**Procédure :**

1. Dans **Settings** → **Identités**
2. Cliquez sur votre identité : `bob@formation.lan`
3. Dans le champ **Signature**, ajoutez :
   ```
   ---
   Bob Martin
   Formation Inc.
   bob@formation.lan
   ```
4. Cochez **Automatically add signature to new messages**
5. Cliquez sur **Save**

6. **Tester la signature**
   - Retournez dans **Mail** → **Compose**
   - La signature doit apparaître automatiquement en bas

---

### Exercice 6.3 : Configurer un message d'absence (vacances)

**Procédure :**

1. **Settings** → **Filters**
2. Cliquez sur l'onglet **Vacation**
3. Cochez **Enable vacation reply**
4. Remplissez :
   - **Subject** : `Absence - Message automatique`
   - **Message** : 
     ```
     Bonjour,
     
     Je suis actuellement absent du bureau.
     Je reviendrai le [date].
     
     Pour toute urgence, contactez equipe@formation.lan
     
     Cordialement,
     Bob Martin
     ```
5. Cliquez sur **Save**

**Test de validation :**

6. **Déconnexion et reconnexion avec Alice**
   - Se déconnecter de Bob
   - Se connecter avec `alice@formation.lan`

7. **Envoyer un email à Bob**
   - **To** : `bob@formation.lan`
   - **Subject** : `Test message d'absence`
   - **Message** : `Test`
   - Cliquez sur **Send**

8. **Observer Terminal 1**

**Logs attendus :**
```
dovecot: lda(bob@formation.lan): sieve: sent vacation response
postfix/smtp: to=<alice@formation.lan>, relay=dovecot, status=sent (vacation reply)
```

9. **Vérifier la réception dans la boîte d'Alice**
   - Rafraîchir la boîte de réception (F5)
   - Vous devriez recevoir la réponse automatique de Bob

**Question :** Avez-vous reçu le message d'absence automatique ?
- ☐ Oui
- ☐ Non

---

## PARTIE 7 : Tests avec Charlie

### Exercice 7.1 : Vérifier les quotas

**Objectif :** Valider que Charlie a reçu les emails et vérifier son quota

**Procédure :**

1. **Se connecter avec Charlie**
   - Username : `charlie@formation.lan`
   - Password : `test123`

2. **Vérifier la réception**
   - Charlie devrait avoir reçu :
     - Email via alias "équipe"
     - Email transféré par Bob (avec pièce jointe)

**Nombre d'emails reçus par Charlie :** ______

3. **Vérifier le quota dans iRedAdmin**
   - Ouvrez iRedAdmin dans un autre onglet
   - Connectez-vous : `postmaster@formation.lan` / `test`
   - Allez dans **Users** → Cliquez sur `charlie@formation.lan`
   - Observez l'utilisation du quota

**Validation dans Terminal 2 :**
```bash
# Voir l'utilisation du quota de Charlie
sudo du -sh /var/vmail/vmail1/formation.lan/c/h/a/charlie-*
```

**Question :** Quelle est l'utilisation actuelle de l'espace disque de Charlie ?
- Réponse : __________ KB/MB

---

## PARTIE 8 : Tests de recherche et filtres

### Exercice 8.1 : Rechercher des emails

**Procédure (connecté avec Bob) :**

1. Dans **Inbox**, utilisez la barre de recherche en haut
2. Tapez : `Alice`
3. Appuyez sur **Entrée**
4. Les résultats s'affichent

**Question :** Combien d'emails sont trouvés ?
- Réponse : __________

5. **Recherche avancée**
   - Cliquez sur l'icône en forme d'entonnoir (à côté de la recherche)
   - Sélectionnez :
     - **Subject** : `pièce jointe`
     - Cliquez sur **Search**

**Question :** L'email "Test 3 - Pièce jointe" est-il trouvé ?
- ☐ Oui
- ☐ Non

---

### Exercice 8.2 : Créer un filtre automatique

**Objectif :** Déplacer automatiquement les emails d'Alice vers le dossier "Projets"

**Procédure :**

1. **Settings** → **Filters**
2. Cliquez sur **Create**
3. Configurez le filtre :
   - **Filter name** : `Emails d'Alice vers Projets`
   - **Scope** : `matching all of the following rules`
   - Règle :
     - **From** → **contains** → `alice@formation.lan`
   - Action :
     - **Move message to** → Sélectionnez `Projets`
4. Cochez **Filter enabled**
5. Cliquez sur **Save**

6. **Tester le filtre**
   - Retournez dans **Mail**
   - Demandez à un collègue de se connecter avec Alice
   - Alice envoie un email à Bob : "Test filtre automatique"

7. **Vérifier**
   - L'email doit arriver directement dans le dossier **Projets**
   - Et non dans **Inbox**

**Question :** Le filtre fonctionne-t-il correctement ?
- ☐ Oui
- ☐ Non

---

## PARTIE 9 : Validation finale et monitoring

### Exercice 9.1 : Statistiques d'utilisation

**Dans Terminal 2 :**

```bash
# 1. Nombre total d'emails dans le système
echo "=== Statistiques du serveur mail ==="
sudo find /var/vmail/vmail1/formation.lan -type f -name "*,S=*" | wc -l

# 2. Espace disque utilisé par domaine
sudo du -sh /var/vmail/vmail1/formation.lan

# 3. Espace disque par utilisateur
echo "=== Utilisation par utilisateur ==="
sudo du -sh /var/vmail/vmail1/formation.lan/*/

# 4. Dernières connexions
echo "=== Dernières connexions ==="
sudo grep "Login:" /var/log/mail.log | tail -10

# 5. Emails envoyés aujourd'hui
echo "=== Emails envoyés aujourd'hui ==="
sudo grep "$(date +%Y-%m-%d)" /var/log/mail.log | grep "status=sent" | wc -l

# 6. Emails en file d'attente
echo "=== File d'attente ==="
sudo postqueue -p
```

**Tableau de résultats :**

| Métrique | Résultat |
|----------|----------|
| Nombre total d'emails | |
| Espace disque total utilisé | |
| Espace disque Alice | |
| Espace disque Bob | |
| Espace disque Charlie | |
| Emails envoyés aujourd'hui | |
| Emails en file d'attente | |

---

### Exercice 9.2 : Vérifier les logs de toutes les opérations

**Dans Terminal 2 :**

```bash
# Résumé des activités par utilisateur
echo "=== Résumé Alice ==="
sudo grep "alice@formation.lan" /var/log/mail.log | grep -E "Login|status=sent|delivered" | tail -20

echo "=== Résumé Bob ==="
sudo grep "bob@formation.lan" /var/log/mail.log | grep -E "Login|status=sent|delivered" | tail -20

echo "=== Résumé Charlie ==="
sudo grep "charlie@formation.lan" /var/log/mail.log | grep -E "Login|status=sent|delivered" | tail -20
```

---

### Exercice 9.3 : Test final - Email groupé

**Objectif :** Valider que tous les utilisateurs peuvent communiquer entre eux

**Procédure :**

1. **Connectez-vous avec Alice**
2. **Composez un email**
   - **To** : `bob@formation.lan, charlie@formation.lan`
   - **Subject** : `Test Final - Validation complète`
   - **Message** : 
     ```
     Bonjour à tous,
     
     Cet email valide que :
     - Alice peut envoyer des emails
     - Bob et Charlie peuvent recevoir des emails
     - Le système de filtrage antivirus fonctionne
     - Les quotas sont respectés
     
     Exercice complété avec succès !
     
     Alice
     ```
   - Cliquez sur **Send**