# infra-ansible-server-setup


:warning: to fix


community.vmware



2degrees linux ansible repo
for all linux servers
https://bitbucket.org/2dgreesdev/td-ansible-server-setup/src/master/README.md 

## BITBUCKET info

### Preparing for intial git clone

#### Set git to use a proxy so we can access bitbucket
```bash
git config --global http.proxy http://frigg.snap.net.nz:3128
```

#### Set yourself a password
on bitbucket go to your settings and generate yourself an "app password" this will be your password when checking out the repo


### Cloning the repo

```bash
git clone https://<username>@bitbucket.org/2dgreesdev/infra-ansible-server-setup.git
cd infra-ansible-server-setup
```

## How to push your changes back to the repo

```bash
git add .
```
```bash
git commit -m "comment about your changes here"
```
```bash
git push
```

# ANSIBLE info

##### vault-password-file
to create/encrypt/decrypt the file, you use:

for new file:
```bash
ansible-vault create testfile.txt --vault-password-file=~/infra-ansible-server-setup/tmp/ansible-vault-file
```
for encrypting existing file:
```bash
ansible-vault encrypt testfile.txt --vault-password-file=~/infra-ansible-server-setup/tmp/ansible-vault-file
```
for decrypting:
```
ansible-vault decrypt testfile.txt --vault-password-file=~/infra-ansible-server-setup/tmp/ansible-vault-file
```
when executing the above, you will notice it doesn't ask for password.


# First time setup

## Lastpass access

Make sure you have access to the `Shared-Techm` folder

## User ssh keys

Make sure you have a rsa ssh key generated and put onto `gary.snap.net.nz:~/.ssh/authorized_keys` so you can authenticate to `gary.snap.net.nz` without a password from the ansible server, else pam_radius config will fail.
```bash
ssh-keygen -t rsa
```
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub gary.snap.net.nz
```

## Required software

```bash
pip3 install --ignore-installed --user PyYAML pwgen
```

```bash
sudo apt install python3-pyvmomi
```

```bash
ansible-galaxy collection install community.vmware
```

# Deploying a new server

:exclamation: Firewall rules, Networking and the domain name to be used, must be complete else deployment will fail:exclamation:

### 1. DNS for servers

Put all vm dns entries fully into dns else deployment will fail
[dnsdb link](https://dnsdb.snap.net.nz)

```bash
cd ~/infra-ansible-server-setup
```

### 2. LastPass access

LastPass access for adding zeus and root passwords/retrieving needed passwords automatically to/from lastpass

#### 2d staff

```bash
env https_proxy="http://frigg.snap.net.nz:3128" lpass login $USER
```

#### techm

```bash
env https_proxy="http://frigg.snap.net.nz:3128" lpass login <techm email>
```



### 3. Virtual machine/s details

* export the spreadsheet as a .csv

* place the csv in the `infra-ansible-server-setup` folder

### 4. Generate Hosts script

This creates all the needed files/variables/passwords for the ansible script

```bash
env https_proxy="http://frigg.snap.net.nz:3128" python generatehosts.py -c filename.csv
```


### 5. Deploy the servers
```bash
ansible-playbook playbooks/newservers.yml --vault-password-file tmp/ansible-vault-file -K
```

