### Updating ansible-galaxy roles

#### Allow the ansible server to talk to ansible galaxy

```bash
export http_proxy=http://frigg.snap.net.nz:3128
export https_proxy=http://frigg.snap.net.nz:3128
```

#### installing a new community role

```bash
ansible-galaxy collection install community.<thing>
```

e.g.

```bash
ansible-galaxy collection install community.vmware
```

