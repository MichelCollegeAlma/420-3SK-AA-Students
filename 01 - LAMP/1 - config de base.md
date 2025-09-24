# 1/5 - Configuration réseau statique sur Ubuntu 24 (VM Proxmox)

## 1) Côté Proxmox
- Vérifier que la machine virtuelle est reliée au bon bridge réseau (exemple : `vmbrX` utilisé pour le réseau étudiant).  
- Le bridge Proxmox permet à la VM d’obtenir une adresse IP sur le même réseau que les autres machines locales.  

---

## 2) Côté Linux (Ubuntu 24)

### Objectif
Fixer une adresse IP statique : `192.168.x.77`

### Étape 1 : Localiser le fichier Netplan
Par défaut, les fichiers Netplan se trouvent dans `/etc/netplan/`.  
On utilisera un fichier de type :
```
/etc/netplan/50-cloud-init.yaml
```

### Étape 2 : Exemple de configuration (Ubuntu 24)
Éditer le fichier avec droits root :
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

Contenu recommandé (adapter `ens18` au nom de l’interface réseau de la VM) :
```yaml
network:
  version: 2
  ethernets:
    ens18:
      dhcp4: false
      addresses:
        - 192.168.x.77/24
      routes:
        - to: default
          via: 192.168.x.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

### Étape 3 : Appliquer la configuration
```bash
sudo netplan apply
```

### Étape 4 : Vérifier l’adresse IP
```bash
ip a
```

La carte réseau doit maintenant avoir l’adresse fixe `192.168.x.77`.

### Étape 5 : Tester avec un ping depuis un poste Windows
Sur l’hôte Windows :
```cmd
ping 192.168.x.77
```
Si la configuration est correcte, la VM répondra.

### Étape 6 : Connexion SSH avec identifiant test/test
Depuis un poste Windows (PowerShell ou CMD) :
```powershell
ssh test@192.168.x.77
```
- Mot de passe : `test`  
- Cela permet de se connecter en ligne de commande à la VM Ubuntu.

---

## Résumé
- **Proxmox** : la VM doit être reliée au bon bridge réseau (réseau étudiant).  
- **Ubuntu (Netplan)** : fixer l’IP via `/etc/netplan/50-cloud-init.yaml` avec l’adresse `192.168.x.77`.  
- **Tests** : ping depuis Windows puis connexion SSH avec `test/test`.  
