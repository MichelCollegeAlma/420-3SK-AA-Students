# Configuration du réseay pour vm ubuntu 24 server

Pour le modifier:

```
sudo nano /etc/netplan/50-cloud-init.yaml
```

Voici la configuration fonctionnel pour le fichier `50-cloud-init.yaml`

```
network:
  version: 2
  renderer: networkd
  ethernets:
    ens18:
      addresses:
        - 192.168.x.12/24
      routes:
        - to: default
          via: 192.168.x.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
          - 192.168.x.1
```
Où *x* est la plage de votre réseau obtenu en sélectionnant le bon bridge (ces informations sont disponibles
[ici](../1.2%20-%20Contexte%20-%20Liste%20des%20sous-r%C3%A9seaux.md)).


Pour appliquer
```
sudo netplan apply
```

Valider ensuite avec ces commandes:
```
ip a
ping google.com
```