# 2/4 - EXAMEN 1 - Tâches

Voici l'idée générale:

Votre réseau utilisera deux serveurs de DNS ainsi qu'un serveur LAMP accessible par vos utilisateurs connecté sous Windows via l'adresse `wiki.votreDA.com` où `votreDA` est remplacé par le vôtre par exemple « tp2.12345678.com ».

Votre travail consiste à configurer votre parc de serveurs pour qu'il soit possible via votre portable étudiant de se connecter au wiki via l'adresse  `wiki.votreDA.lan` sans utiliser l'adresse IP du serveur.

Voici les caractéristiques des trois serveurs:

| Type de serveur | Nom de l'hôte          | Nom de la VM           | IP             |
|:----------------|:-----------------------|:-----------------------|:---------------|
| DNS PRIMAIRE    | examen1-dns-primaire   | examen1-dns-primaire   | 192.168.*x*.20 |
| DNS SECONDAIRE  | examen1-dns-secondaire | examen1-dns-secondaire | 192.168.*x*.21 |
| LAMP            | examen1-lamp           | examen1-lamp           | 192.168.*x*.22 |

Où *x* est votre propre réseau.

### À faire
- Vous devez créez de nouvelles installations ou vous baser sur le template d'installation Ubuntu 24 fournie.
- Vous devez utiliser la dernière version disponible de MediaWiki.
- Pour chaques serveurs, vous devez documenter les services et configurations utilisés tel que les noms d'utilisateurs et mot de passes.
  - Utilisez le projet GitHub en créant un dossier `EXAMEN 1`. 
  - Utilisez les identifiants `test`/`test` tout au long de votre projet. S'il n'est pas possible de le faire, indiquer le clairement dans votre documentation.
  - Indiquez l'URL pour atteindre votre page.

### Durée
- Vous avez 5 heures pour effectuer le travail demandé.
  - Lundi, le 20 octobre, de 10:30 à 12:30.
  - Mercredi, le 22 octobre, de 8:30 à 11:30.

### Contexte de réalisation
- Le travail ce fait seul
- Vous avez le droit à toute la documentation que vous souhaitez.
- Je réponds pas aux questions sur comment réaliser les tâches.
