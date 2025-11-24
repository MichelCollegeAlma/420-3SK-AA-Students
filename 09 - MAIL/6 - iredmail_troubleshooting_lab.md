# Exercice de dépannage iRedMail
## Test et résolution de problèmes d'envoi d'emails

---

## Objectifs de l'exercice

À la fin de cet exercice, vous serez capable de :
1. Tester l'envoi d'emails via l'interface Roundcube
2. Monitorer les logs en temps réel sur le serveur
3. Identifier et résoudre les problèmes d'envoi d'emails
4. Comprendre l'architecture des services mail (Postfix, Dovecot, Amavis, ClamAV)
5. Utiliser plusieurs terminaux SSH simultanément pour le diagnostic

---

## Prérequis

- Serveur iRedMail installé et configuré (mail.formation.lan)
- Accès SSH au serveur avec l'utilisateur `test`
- Au moins un compte email créé (ex: test@formation.lan)
- Navigateur web pour accéder à Roundcube

---

## Matériel nécessaire

- **2 terminaux SSH** ouverts simultanément sur le serveur mail
- **1 navigateur web** pour accéder à Roundcube

---

## Partie 1 : Configuration de l'environnement de test

### Étape 1.1 : Ouvrir deux sessions SSH

**Terminal 1 - Surveillance des logs**
```bash
ssh test@mail.formation.lan
```

**Terminal 2 - Commandes de diagnostic**
```bash
ssh test@mail.formation.lan
```

### Étape 1.2 : Vérifier les comptes utilisateurs existants

Dans le **Terminal 2**, vérifiez les comptes email disponibles :

```bash
sudo mysql -u root -ptest -e "USE vmail; SELECT username, active FROM mailbox;"
```

**Questions :**
1. Combien de comptes email sont actifs ?
2. Notez les adresses email disponibles pour le test

### Étape 1.3 : Créer un compte de test supplémentaire (optionnel)

Si vous n'avez qu'un seul compte, créez-en un second via iRedAdmin :

1. Accédez à https://mail.formation.lan/iredadmin
2. Connectez-vous avec `postmaster@formation.lan` / `test`
3. Créez un utilisateur `utilisateur2@formation.lan`

---

## Partie 2 : Test d'envoi d'email avec monitoring

### Étape 2.1 : Démarrer le monitoring en temps réel

Dans le **Terminal 1**, lancez la surveillance des logs :

```bash
sudo tail -f /var/log/mail.log
```

⚠️ **Important :** Laissez ce terminal ouvert et visible pendant tout l'exercice.

### Étape 2.2 : Vérifier l'état des services

Dans le **Terminal 2**, vérifiez que tous les services sont actifs :

```bash
# Vérifier Postfix (serveur SMTP)
sudo systemctl status postfix | grep Active

# Vérifier Dovecot (serveur IMAP)
sudo systemctl status dovecot | grep Active

# Vérifier Amavis (antivirus/antispam)
sudo systemctl status amavis | grep Active

# Vérifier ClamAV (antivirus)
sudo systemctl status clamav-daemon | grep Active

# Vérifier PHP-FPM (pour Roundcube)
sudo systemctl status php8.3-fpm | grep Active

# Vérifier iRedAdmin
sudo systemctl status iredadmin | grep Active
```

**Tableau à remplir :**

| Service | État (active/inactive) | Port(s) utilisé(s) |
|---------|------------------------|-------------------|
| Postfix | | 25, 587 |
| Dovecot | | 143, 993 |
| Amavis | | 10024, 10026 |
| ClamAV | | (socket) |
| PHP-FPM | | 9999 |
| iRedAdmin | | 7791 |

### Étape 2.3 : Vérifier les ports réseau

Dans le **Terminal 2**, vérifiez que les ports sont ouverts :

```bash
# Ports SMTP
sudo ss -tlnp | grep -E ":25|:587"

# Ports IMAP
sudo ss -tlnp | grep -E ":143|:993"

# Ports Amavis
sudo ss -tlnp | grep -E ":10024|:10026"

# Port PHP-FPM
sudo ss -tlnp | grep :9999

# Port iRedAdmin
sudo ss -tlnp | grep :7791
```

**Questions :**
1. Tous les ports sont-ils ouverts et en écoute ?
2. Si un port est manquant, quel service doit être redémarré ?

---

## Partie 3 : Premier test d'envoi d'email

### Étape 3.1 : Se connecter à Roundcube

1. Ouvrez votre navigateur web
2. Accédez à : `https://mail.formation.lan/mail`
3. Acceptez l'avertissement de sécurité SSL
4. Connectez-vous avec :
   - **Username :** `test@formation.lan`
   - **Password :** (votre mot de passe)

### Étape 3.2 : Composer un email de test

1. Cliquez sur **Compose** (Rédiger)
2. Remplissez :
   - **To :** `utilisateur2@formation.lan` (ou votre second compte)
   - **Subject :** `Test 1 - Envoi d'email`
   - **Message :** `Ceci est un email de test pour vérifier le fonctionnement du serveur mail.`
3. Cliquez sur **Send** (Envoyer)

### Étape 3.3 : Observer les logs dans le Terminal 1

**Observez attentivement le Terminal 1** pendant l'envoi.

**Logs attendus (si tout fonctionne) :**

```
postfix/submission/smtpd[xxxxx]: connect from localhost[127.0.0.1]
postfix/submission/smtpd[xxxxx]: Anonymous TLS connection established
postfix/submission/smtpd[xxxxx]: client=localhost[127.0.0.1], sasl_method=LOGIN, sasl_username=test@formation.lan
postfix/cleanup[xxxxx]: message-id=<...>
roundcube: User test@formation.lan; Message <...> for utilisateur2@formation.lan; 250: 2.0.0 Ok: queued
postfix/qmgr[xxxxx]: from=<test@formation.lan>, size=XXX, nrcpt=1 (queue active)
postfix/amavis/smtp[xxxxx]: Relayed to [127.0.0.1]:10024
amavis[xxxxx]: Passed CLEAN
postfix/smtp[xxxxx]: status=sent (delivered to mailbox)
```

**Questions d'analyse :**
1. Voyez-vous la ligne "connect from localhost" ?
2. Voyez-vous "sasl_username=test@formation.lan" ?
3. Voyez-vous "250: 2.0.0 Ok: queued" ?
4. Voyez-vous "Passed CLEAN" (filtrage Amavis) ?
5. Voyez-vous "status=sent" ?

---

## Partie 4 : Scénarios de pannes et résolution

### Scénario 1 : Erreur "Connection refused" (SMTP)

**Symptôme :** Message d'erreur dans Roundcube : "SMTP Error: Connection failed"

**Logs observés dans Terminal 1 :**
```
roundcube: PHP Error: Connection refused
roundcube: SMTP Error: Connection failed: (Code: -1)
```

**Diagnostic dans Terminal 2 :**

```bash
# 1. Vérifier si Postfix écoute sur le port 587
sudo ss -tlnp | grep :587
```

**Question :** Le port 587 est-il ouvert ?
- ☐ Oui → Passer au scénario suivant
- ☐ Non → Appliquer la correction ci-dessous

**Correction :**

```bash
# Redémarrer Postfix
sudo systemctl restart postfix

# Vérifier à nouveau le port
sudo ss -tlnp | grep :587

# Vérifier le statut
sudo systemctl status postfix
```

**Test :** Réessayez d'envoyer un email depuis Roundcube.

---

### Scénario 2 : Erreur "Unsupported authentication mechanism"

**Symptôme :** Impossible de se connecter à Roundcube avec le message "Authentication failed"

**Logs observés dans Terminal 1 :**
```
dovecot: imap-login: Disconnected: Connection closed (tried to use unsupported auth mechanism)
roundcube: IMAP Error: Login failed... Unsupported authentication mechanism
```

**Diagnostic dans Terminal 2 :**

```bash
# Vérifier les mécanismes d'authentification activés
sudo grep "auth_mechanisms" /etc/dovecot/conf.d/10-auth.conf
```

**Question :** La ligne contient-elle "login" ?

**Correction :**

```bash
# Éditer la configuration
sudo nano /etc/dovecot/conf.d/10-auth.conf

# Chercher la ligne auth_mechanisms et modifier pour :
# auth_mechanisms = plain login

# Sauvegarder (Ctrl+O, Entrée, Ctrl+X)

# Redémarrer Dovecot
sudo systemctl restart dovecot
```

**Test :** Reconnectez-vous à Roundcube.

---

### Scénario 3 : Email bloqué par Amavis (Connection refused port 10026)

**Symptôme :** L'email semble envoyé mais n'arrive jamais. Message "deferred" dans les logs.

**Logs observés dans Terminal 1 :**
```
postfix/qmgr: from=<test@formation.lan>, size=XXX, nrcpt=1 (queue active)
postfix/amavis/smtp: connect to 127.0.0.1[127.0.0.1]:10026: Connection refused
postfix/amavis/smtp: status=deferred (connect to 127.0.0.1:10026: Connection refused)
```

**Diagnostic dans Terminal 2 :**

```bash
# 1. Vérifier si Amavis écoute sur les ports
sudo ss -tlnp | grep -E "10024|10026"
```

**Question :** Les ports 10024 et 10026 sont-ils ouverts ?
- ☐ Oui → Le problème est ailleurs
- ☐ Non → Appliquer les corrections ci-dessous

**Étape 1 : Vérifier ClamAV**

```bash
# ClamAV doit être démarré pour qu'Amavis fonctionne
sudo systemctl status clamav-daemon
```

**Si ClamAV est inactif :**

```bash
# Démarrer ClamAV
sudo systemctl start clamav-daemon
sudo systemctl enable clamav-daemon

# Vérifier le statut
sudo systemctl status clamav-daemon
```

**Étape 2 : Vérifier les répertoires Amavis**

```bash
# Vérifier si les répertoires existent
sudo ls -la /var/lib/amavis/
```

**Si les répertoires n'existent pas :**

```bash
# Créer les répertoires
sudo mkdir -p /var/lib/amavis/tmp
sudo mkdir -p /var/lib/amavis/db
sudo mkdir -p /var/lib/amavis/virusmails

# Donner les permissions
sudo chown -R amavis:amavis /var/lib/amavis
sudo chmod 750 /var/lib/amavis
sudo chmod 750 /var/lib/amavis/tmp
```

**Étape 3 : Redémarrer Amavis**

```bash
# Redémarrer Amavis
sudo systemctl restart amavis

# Vérifier que les ports sont maintenant ouverts
sudo ss -tlnp | grep -E "10024|10026"

# Vérifier le statut
sudo systemctl status amavis
```

**Test :** Réessayez d'envoyer un email depuis Roundcube.

---

### Scénario 4 : Roundcube inaccessible (502 Bad Gateway)

**Symptôme :** Impossible d'accéder à https://mail.formation.lan/mail (erreur 502)

**Diagnostic dans Terminal 2 :**

```bash
# 1. Vérifier PHP-FPM
sudo systemctl status php8.3-fpm

# 2. Vérifier que PHP-FPM écoute sur le port 9999
sudo ss -tlnp | grep 9999
```

**Correction :**

```bash
# Redémarrer PHP-FPM
sudo systemctl restart php8.3-fpm

# Vérifier le port
sudo ss -tlnp | grep 9999

# Redémarrer Nginx
sudo systemctl restart nginx
```

**Test :** Accédez à nouveau à Roundcube dans votre navigateur.

---

### Scénario 5 : iRedAdmin inaccessible (502 Bad Gateway)

**Symptôme :** Impossible d'accéder à https://mail.formation.lan/iredadmin

**Diagnostic dans Terminal 2 :**

```bash
# Vérifier le service iRedAdmin
sudo systemctl status iredadmin

# Vérifier le port 7791
sudo ss -tlnp | grep 7791
```

**Correction :**

```bash
# Démarrer iRedAdmin
sudo systemctl start iredadmin
sudo systemctl enable iredadmin

# Vérifier le port
sudo ss -tlnp | grep 7791
```

**Test :** Accédez à nouveau à iRedAdmin dans votre navigateur.

---

## Partie 5 : Vérification complète du système

### Étape 5.1 : Liste de vérification (Checklist)

Complétez cette liste de vérification dans le **Terminal 2** :

```bash
echo "=== VÉRIFICATION COMPLÈTE DU SERVEUR MAIL ==="
echo ""

echo "1. Services actifs :"
sudo systemctl is-active postfix dovecot nginx mariadb amavis clamav-daemon php8.3-fpm iredadmin iredapd

echo ""
echo "2. Ports en écoute :"
echo "Port 25 (SMTP):"
sudo ss -tlnp | grep :25
echo "Port 587 (Submission):"
sudo ss -tlnp | grep :587
echo "Port 143 (IMAP):"
sudo ss -tlnp | grep :143
echo "Port 993 (IMAPS):"
sudo ss -tlnp | grep :993
echo "Ports 10024/10026 (Amavis):"
sudo ss -tlnp | grep -E "10024|10026"

echo ""
echo "3. File d'attente mail :"
sudo postqueue -p
```

### Étape 5.2 : Test complet d'envoi et réception

**Test 1 : Email local (même domaine)**

1. Connectez-vous à Roundcube avec `test@formation.lan`
2. Envoyez un email à `utilisateur2@formation.lan`
3. Observez les logs dans Terminal 1
4. Connectez-vous avec le compte `utilisateur2@formation.lan`
5. Vérifiez la réception de l'email

**Test 2 : Email avec pièce jointe**

1. Composez un nouvel email
2. Ajoutez une petite pièce jointe (image, PDF)
3. Envoyez l'email
4. Observez dans les logs que le fichier passe par Amavis (scan antivirus)

**Test 3 : Vérification de la file d'attente**

Dans le **Terminal 2** :
```bash
# Vérifier qu'aucun email n'est bloqué
sudo postqueue -p

# Résultat attendu : "Mail queue is empty"
```

---

## Partie 6 : Questions de synthèse

### Questions techniques

1. **Dans quel ordre les services traitent-ils un email sortant ?**
   - Réponse : _______________________________________________

2. **Quel port utilise Roundcube pour envoyer des emails ?**
   - ☐ Port 25
   - ☐ Port 587
   - ☐ Port 465

3. **Quel service est responsable de l'antivirus ?**
   - Réponse : _______________________________________________

4. **Que signifie "status=deferred" dans les logs ?**
   - Réponse : _______________________________________________

5. **Quelle commande permet de voir les emails en attente ?**
   - Réponse : _______________________________________________

### Questions de dépannage

**Scénario A :** Un utilisateur se plaint qu'il ne peut pas envoyer d'emails. Vous voyez cette ligne dans les logs :
```
postfix/amavis/smtp: connect to 127.0.0.1:10026: Connection refused
```

**Question :** Quelle est la cause probable et quelle est la solution ?
- Réponse : _______________________________________________

**Scénario B :** Vous voyez cette erreur dans les logs :
```
dovecot: imap-login: Disconnected: Connection closed (tried to use unsupported auth mechanism)
```

**Question :** Que devez-vous modifier et dans quel fichier ?
- Réponse : _______________________________________________

---

## Partie 7 : Commandes de dépannage avancées

### Diagnostic approfondi

```bash
# 1. Voir les 100 dernières lignes des logs mail
sudo tail -100 /var/log/mail.log

# 2. Filtrer les erreurs uniquement
sudo grep -i error /var/log/mail.log | tail -20

# 3. Voir les connexions SMTP en temps réel
sudo journalctl -u postfix -f

# 4. Tester l'authentification SMTP manuellement
telnet localhost 587
# Tapez : EHLO localhost
# Observez les mécanismes d'authentification disponibles

# 5. Vérifier la configuration Postfix
sudo postconf | grep -E "smtpd_sasl|submission"

# 6. Forcer l'envoi des emails en file d'attente
sudo postqueue -f

# 7. Supprimer tous les emails en file d'attente (ATTENTION)
sudo postsuper -d ALL
```

---

## Grille d'évaluation

### Compétences évaluées

| Critère | Points | Auto-évaluation |
|---------|--------|-----------------|
| Ouverture de 2 terminaux SSH simultanés | /5 | |
| Surveillance des logs en temps réel | /10 | |
| Identification des services nécessaires | /10 | |
| Vérification des ports réseau | /10 | |
| Diagnostic d'erreur SMTP | /15 | |
| Résolution du problème Amavis | /15 | |
| Résolution du problème Dovecot | /10 | |
| Test d'envoi d'email réussi | /15 | |
| Compréhension du flux d'email | /10 | |
| **TOTAL** | **/100** | |

---

## Ressources complémentaires

### Fichiers de configuration importants

```
/etc/postfix/main.cf          # Configuration principale Postfix
/etc/postfix/master.cf        # Services Postfix
/etc/dovecot/dovecot.conf     # Configuration Dovecot
/etc/dovecot/conf.d/10-auth.conf  # Authentification Dovecot
/etc/amavis/conf.d/50-user    # Configuration Amavis
/etc/nginx/sites-enabled/     # Configuration Nginx
/opt/www/roundcubemail/config/config.inc.php  # Configuration Roundcube
```

### Logs importants

```
/var/log/mail.log             # Tous les logs mail (Postfix, Dovecot, Amavis)
/var/log/nginx/error.log      # Erreurs Nginx
/var/log/nginx/access.log     # Accès Nginx
/var/log/syslog               # Logs système généraux
```

### Commandes de diagnostic rapide

```bash
# Status de tous les services mail
sudo systemctl status postfix dovecot amavis clamav-daemon nginx php8.3-fpm iredadmin

# Tous les ports mail en écoute
sudo ss -tlnp | grep -E ":25|:587|:143|:993|:10024|:10026|:7791|:9999"

# Dernières erreurs mail
sudo grep -i error /var/log/mail.log | tail -20
```

---

## Conclusion

Cet exercice vous a permis de :
- ✅ Comprendre l'architecture d'un serveur mail complet
- ✅ Utiliser plusieurs terminaux SSH pour le monitoring
- ✅ Identifier et résoudre des problèmes courants
- ✅ Interpréter les logs en temps réel
- ✅ Maîtriser les commandes de diagnostic

**Félicitations ! Vous êtes maintenant capable de dépanner un serveur iRedMail.**

---

## Pour aller plus loin

1. **Testez l'envoi vers un domaine externe** (ex: Gmail, Outlook)
2. **Configurez des alias** et testez la redirection
3. **Créez une liste de diffusion** et testez l'envoi groupé
4. **Simulez une panne** en arrêtant un service et résolvez-la
5. **Analysez les performances** avec `pflogsumm`

**Bon courage dans vos dépannages futurs !** 🚀📧