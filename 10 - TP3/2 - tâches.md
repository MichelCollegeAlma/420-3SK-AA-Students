# 2/5 - TP6 - Tâches

Voici l'idée générale:

Votre réseau utilisera **un serveur DNS** (déjà configurés), **un serveur mail** et **des comptes utilisateurs** accessibles via l'interface web Roundcube à l'adresse `https://mail.formation.lan/mail`.


Votre travail consiste à :
1. Configurer le serveur DNS pour le serveur mail
2. Installer et configurer iRedMail sur Ubuntu Server 24.04
3. Créer au moins 3 comptes utilisateurs
4. Tester l'envoi et la réception d'emails entre utilisateurs
5. Documenter toute la configuration
6. Effectuer tous les tests demandés

### Caractéristiques du serveur mail :

| Type de serveur | Nom de l'hôte | IP   | FQDN |
|:----------------|:--------------|:-----|:-----|
| **Mail** | mail | DHCP | mail.formation.lan |

**Domaine mail :** `formation.lan`

**Utilisateurs à créer :**
- `cric@formation.lan` (mot de passe : `test123`)
- `crac@formation.lan` (mot de passe : `test123`)
- `croc@formation.lan` (mot de passe : `test123`)
![img.png](images/criccraccroc.png)

**Alias à créer :**
- `equipe@formation.lan` → Redirige vers cric et croc

**Services requis :**
- Postfix (SMTP)
- Dovecot (IMAP/POP3)
- Roundcube (Webmail)
- iRedAdmin (Administration)

### Prérequis

Vous devez avoir :
- Un serveurs DNS fonctionnel
- Une VM Ubuntu Server 24.04 fraîchement installée
- Accès à votre environnement Proxmox
- Connexion SSH fonctionnelle

⚠️ **Important :** Suivez les guides fournis dans l'ordre pour éviter les erreurs.


## Conseils

- **Lisez tous les guides** avant de commencer
- **Soyez patient** : La propagation DNS peut prendre quelques minutes
- **Utilisez 2 terminaux SSH** : Un pour les logs, un pour les commandes
- **Documentez au fur et à mesure** : Ne pas attendre la fin
- **Testez chaque étape** avant de passer à la suivante
- **Faites des snapshots** de votre VM aux étapes clés
- **Consultez les logs** en cas de problème : `/var/log/mail.log`
