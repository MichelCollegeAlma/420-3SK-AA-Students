# Conteneurisation vs Virtualisation

## Contexte général
Les deux technologies — ls **contrneurisation** et la **virtualisation** — servent à **isoler** des environnements afin d’exécuter plusieurs applications ou systèmes indépendamment sur la même machine physique.

👉 Mais elles le font à des **niveaux différents de la pile logicielle**.

---

## Virtualisation classique (VMs)

### Principe
La **virtualisation** repose sur un **hyperviseur** (comme **VMware**, **VirtualBox**, **Proxmox**, **KVM**, **Hyper-V**, etc.) qui permet de créer des **machines virtuelles (VM)**.
Chaque VM simule un **ordinateur complet**.

### Architecture
```
[Matériel physique]
       │
 ┌─────▼─────┐
 │Hyperviseur│
 └─────┬─────┘
   │       │
   ▼       ▼
[VM1]    [VM2]
 OS1      OS2
 Apps     Apps
```

### Caractéristiques
- Chaque VM a son **propre système d’exploitation complet**.
- Le **noyau du système** est **dupliqué** pour chaque VM.
- L’hyperviseur attribue **CPU, RAM, disque, interfaces réseau** virtuelles à chaque VM.

### Avantages
✅ Très **isolé**.
✅ Permet de faire tourner différents **OS**.
✅ Bon pour simuler un réseau complet.

### Inconvénients
❌ Lourd : chaque VM charge un OS complet.
❌ Temps de démarrage long.
❌ Redondance de bibliothèques et fichiers systèmes.

---

## Conteneurisation (Docker, Podman, Kubertenes)

### Principe
La Conteneurisation n’émule pas une machine complète : il **partage le noyau du système hôte**.
Chaque conteneur est une **application isolée** avec ses **dépendances**, mais sans système d’exploitation complet.

### Architecture
```
    [Matériel physique]
           │
      [OS hôte Linux]
           │
     ┌─────▼─────────┐
     │ Docker Daemon │
     └─┬─────────┬───┘
       │         │
       ▼         ▼
[Conteneur A]   [Conteneur B]
App + Libs      App + Libs
```

### Caractéristiques
- Tous les conteneurs partagent le **même noyau Linux**.
- Chaque conteneur a sa propre **vue du système de fichiers**, des **processus**, du **réseau**.
- L’isolation repose sur des **namespaces** et des **cgroups**.

### Avantages
✅ Très **léger**.
✅ Démarrage quasi instantané.
✅ Facile à **déployer, reproduire et migrer**.
✅ Idéal pour le **développement** et les **microservices**.

### Inconvénients
❌ Moins isolé qu’une VM.
❌ Ne peut pas exécuter un OS différent du noyau hôte.
❌ Besoin de configuration fine pour la sécurité.

---

## Comparatif Conteneurisation vs Virtualisation

| Critère | **Virtualisation (VM)** | **Conteneurisation (Docker)** |
|----------|--------------------------|-------------------------------|
| **Niveau d’isolation** | Fort (OS complet par VM) | Léger (partage du noyau) |
| **Système d’exploitation invité** | Complet et indépendant | Aucun (partage du noyau hôte) |
| **Démarrage** | Lent | Très rapide |
| **Ressources utilisées** | Lourdes | Légères |
| **Portabilité** | Moyenne | Très élevée |
| **Sécurité** | Très forte | Bonne, dépend du confinement |
| **Cas d’usage typique** | Héberger des serveurs, tester plusieurs OS | Microservices, CI/CD, dev/test rapide |

---

## Exemple concret

### VM
> Vous créez une VM Ubuntu complète avec Apache.
> Elle a 2 Go de RAM, un disque virtuel de 20 Go, et son propre noyau.

### Conteneur
> Vous exécutez `docker run -d apache:latest`
> Cela démarre un conteneur Apache en **moins d’une seconde**, utilisant à peine quelques Mo.

---

## Métaphore
- **Virtualisation** = chaque client a **sa maison complète**.
- **Docker** = chaque client loue **un appartement dans un immeuble partagé**.

---

## Cas d’utilisation typiques

| Cas d’usage | Recommandé |
|--------------|------------|
| Laboratoires réseau, serveurs, OS différents | **Virtualisation** |
| Déploiement d’applications web | **Docker** |
| Simulation d’infrastructure complète | **VMs ou Proxmox + Docker combinés** |
| Microservices (API, front, DB séparés) | **Docker Compose / Kubernetes** |

---
