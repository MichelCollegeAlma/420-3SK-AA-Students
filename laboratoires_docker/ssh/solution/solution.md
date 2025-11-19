# Docker et SSH - Solutions

## Environment
Démarrez l’environnement :
   ```bash
   docker compose up -d
   docker compose ps
```

## Test des connections
Depuis la machine hôte, testez les connexions SSH :
```bash
ssh -p 2222 clientPing@localhost
ssh -p 2223 clientPong@localhost
ssh -p 2224 clientTest@localhost
```

Sur clientTest:
```
ssh -p 2224 clientTest@localhost
ssh -p 2222 clientPing@172.20.0.10
ssh -p 2223 clientPong@172.20.0.11
```

Sur clientPing:
```
ssh -p 2224 clientTest@172.20.0.12
ssh -p 2222 clientPing@localhost
ssh -p 2223 clientPong@172.20.0.11
```

Sur clientP0ng:
```
ssh -p 2224 clientTest@172.20.0.12
ssh -p 2222 clientPing@172.20.0.11
ssh -p 2223 clientPong@localhost
```


## Génération et échange des clés publiques

Dans **chacun** des conteneurs, exécutez :
```bash
ssh-keygen -t ed25519 -a 100 -C "nom@lab"

i.e.:
ssh-keygen -t ed25519 -a 100 -C "clientPing@lab"
ssh-keygen -t ed25519 -a 100 -C "clientPong@lab"
ssh-keygen -t ed25519 -a 100 -C "clientTest@lab"

```

Vérifiez les permissions dans **chaque** conteneurs:
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

### a) `clientPing` → `clientPong`
```bash
ssh-copy-id -p 2223 -i ~/.ssh/id_ed25519.pub clientPong@172.20.0.11
```

### b) `clientPong` → `clientPing`
```bash
ssh-copy-id -p 2222 -i ~/.ssh/id_ed25519.pub clientPing@172.20.0.10
```

### c) `clientTest` → `clientPing` et `clientPong`
```bash
ssh-copy-id -p 2222 -i ~/.ssh/id_ed25519.pub clientPing@172.20.0.10
ssh-copy-id -p 2223 -i ~/.ssh/id_ed25519.pub clientPong@172.20.0.11
```

## Test de connexion sans mot de passe

Depuis chaque conteneur :
```bash
ssh -p 2222 clientPing@172.20.0.10
ssh -p 2223 clientPong@172.20.0.11
ssh -p 2224 clientTest@172.20.0.12
```
Aucune demande de mot de passe = **succès de l’authentification par clé publique** 🎉

