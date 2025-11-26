# Problème de DHCP

Vous ne réussissez pas à avoir un ip valida en DHCP ?

1. Dans la VM, assurez-vous d'être en DHCP
2. Sur Proxmox, dans Hardware, modifier le bridge de la VM pour **vmbr1**
2. Dans la VM, `Sudo netplan apply`
3. Dans la VM, validez avec `ip a`
2. Sur Proxmox, dans Hardware, modifier le bridge de la VM pour **vmbr0**
2. Dans la VM, `Sudo netplan apply`
3. Dans la VM, validez avec `ip a`
3. Dans la VM, Testez `ping google.com`

Le problème devrait être corrigé, retentez une connection *SSH*