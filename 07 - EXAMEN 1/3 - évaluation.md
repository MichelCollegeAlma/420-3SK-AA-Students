# 3/4 - EXAMEN 1 - Évaluation

Vous serez évaluez à partir de votre environnement Proxmox et de votre projet GitHub « 3SK-VotreDA ».

- Crée le dossier `EXAMEN 1` et dans ce dossier, créer les sous-dossiers demandés dans la partie `2 - tâches`.

## Grille de correction

| Serveur/Poste  | Catégorie            | Description                               | Points | Total  |
|:---------------|:---------------------|:------------------------------------------|:-------|:-------|
| Proxmox        | Config VM            | examen1-dns-primaire                      |   | 1 pt   |
| Proxmox        | Config VM            | examen1-dns-secondaire                    |   | 1 pt   |
| Proxmox        | Config VM            | examen1-lamp                              |   | 1 pt   |
| DNS primaire   | Nom d'hôte           | examen1-dns-primaire                      |   | 1 pt   |
| DNS primaire   | fichier config (.md) | * infos spécifique                        |   | 2 pts  |
| DNS primaire   | IP statique          | 192.168.x.20                              |   | 1 pt   |
| DNS primaire   | DNS                  | wiki.votreDA.com                          |   | 2 pts  |
| DNS primaire   | Config               | serveur DNS primaire                      |   | 10 pts |
| DNS primaire   | Test                 | ping votreDA.com                          |   | 1 pt   |
| DNS primaire   | Test                 | ping wiki.votreDA.com                     |   | 1 pt   |
| DNS primaire   | Test                 | named-checkconf -z                        |   | 1 pt   |
| DNS primaire   | Test                 | nslookup votreDA.com                      |   | 1 pt   |
| DNS secondaire | Nom d'hôte           | examen1-dns-secondaire                    |   | 1 pt   |
| DNS secondaire | fichier config (.md) | * infos spécifique                        |   | 2 pts  |
| DNS secondaire | IP statique          | 192.168.x.21                              |   | 1 pt   |
| DNS secondaire | DNS                  | wiki.votreDA.com                          |   | 2 pts  |
| DNS secondaire | Config               | serveur DNS secondaire                    |   | 6 pts  |
| DNS secondaire | Test                 | ping votreDA.com                          |   | 1 pt   |
| DNS secondaire | Test                 | ping wiki.votreDA.com                     |   | 1 pt   |
| DNS secondaire | Test                 | named-checkconf -z                        |   | 1 pt   |
| DNS secondaire | Test                 | nslookup votreDA.com                      |   | 1 pt   |
| DNS LAMP       | Nom d'hôte           | examen1-lamp                              |   | 1 pt   |
| DNS LAMP       | fichier config (.md) | * infos spécifique                        |   | 2 pts  |
| DNS LAMP       | IP statique          | 192.168.x.22                              |   | 1 pt   |
| DNS LAMP       | Config               | serveur DNS LAMP                          |   | 16 pts |
| DNS LAMP       | Test                 | ping votreDA.com                          |   | 1 pt   |
| DNS LAMP       | Test                 | ping wiki.votreDA.com                     |   | 1 pt   |
| DNS LAMP       | Test                 | nslookup votreDA.com                      |   | 1 pt   |
| Poste          | Navigateur           | http://wiki.votreDA.com                   |   | 10 pts |
| GitHub         | Documentation        | Qualité et pertinence de la documentation |   | 10 pts |
|                |                      | TOTAL                                     |   | 82 pts |