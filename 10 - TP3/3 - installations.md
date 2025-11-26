# 2/6 - TP3 - Instalaltions

### Phase 1 : Installation et configuration de base

1. Configurez le DNS adéquatement
2. Option 1 - Utilisez votre VM déjà fonctionnelle.
    1. Renommez la VM `MAIL-US24`
    1. Utilisez un IP dynamique
    1. Vérifier que tous les services sont actifs
3. Option 2 - Créez une nouvelle VM
    1. Créer la VM `MAIL-US24` avec Ubuntu Server 24.04
    1. Utilisez un IP dynamique
    1. Configurer le hostname `mail` et le FQDN `mail.formation.lan`
    1. Installer iRedMail avec tous les composants
    1. Vérifier que tous les services sont actifs

### Phase 2 : Création des utilisateurs

1. Se connecter à iRedAdmin (`https://mail.formation.lan/iredadmin`)
2. Créer les 3 utilisateurs : cric, crac, croc
3. Créer l'alias `equipe@formation.lan`
4. Vérifier la création dans la base de données MariaDB