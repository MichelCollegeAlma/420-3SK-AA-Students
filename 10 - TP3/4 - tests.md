# 4/6 - TP3 - Tests à effectuer

Voici les différents tests effectués lors des phases du projet.

**Certains tests doivent être documentés, voir [5-documentation](5%20-%20documentation.md) pour savoir lesquels et ne pas travailler pour rien.**

### Phase 1 : Tests d'envoi et réception

**Terminal 1 : Monitoring**
```bash
ssh test@mail.formation.lan
sudo tail -f /var/log/mail.log
```

**Terminal 2 : Tests**
```bash
ssh test@mail.formation.lan
# Commandes de vérification
```

**Navigateur : Roundcube**
- Test 1 : cric envoie un email à crac
- Test 2 : crac répond à cric
- Test 3 : cric envoie un email avec pièce jointe à croc
- Test 4 : crac envoie un email à `equipe@formation.lan`
- Test 5 : croc transfère un email à cric

### Phase 2 : Tests des fonctionnalités

1. Créer des dossiers personnalisés (Projets, Archives)
2. Déplacer des emails dans les dossiers
3. Ajouter des contacts au carnet d'adresses
4. Configurer une signature email
5. Tester la recherche d'emails
6. Créer un filtre automatique

### Phase 3 : Administration

1. Modifier un quota utilisateur via iRedAdmin
2. Vérifier l'utilisation disque des utilisateurs
3. Consulter les statistiques du serveur
4. Vérifier la file d'attente mail
5. Analyser les logs pour un utilisateur spécifique
