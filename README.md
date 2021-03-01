# td-ansible-server-setup
2degrees linux ansible repo
for all linux servers
https://bitbucket.org/2dgreesdev/td-ansible-server-setup/src/master/README.md 

## BITBUCKET info

### Preparing for intial git clone

#### Set git to use a proxy so we can access bitbucket
git config --global http.proxy http://frigg.snap.net.nz:3128

#### Set yourself a password
on bitbucket go to your settings and generate yourself an "app password" this will be your password when checking out the repo


### Cloning the repo

```

git clone https://<username>@bitbucket.org/2dgreesdev/infra-ansible-server-setup.git

```

## How to push your changes back to the repo

```
git add .

git commit -m "comment about your changes here"

git push

```

# ANSIBLE info

### updating ansible-galaxy roles

#### allow the ansible server to talk to ansible galaxy
```
export http_proxy=http://frigg.snap.net.nz:3128
export https_proxy=https://frigg.snap.net.nz:3128
```
#### installing a new community role
```
ansible-galaxy collection install community.****
```
### e.g.
```
ansible-galaxy collection install community.vmware
```
##### ansible-vault-passwords file
to create/encrypt/decrypt the file, you use:

for new file:
```
ansible-vault create testfile.txt --vault-password-file=ansible-vault-file
```
for encrypting existing file:
```
ansible-vault encrypt testfile.txt --vault-password-file=ansible-vault-file
```
for decrypting:
```
ansible-vault decrypt testfile.txt --vault-password-file=ansible-vault-file
```
when executing the above, you will notice it doesn't ask for password.


# First time setup

## User ssh keys

make sure you have a rsa ssh key generated and put onto gary so you can authenticate to gary without a password, else pam_radius config will failmake sure you have created a personal.yml file from personal.yml.example and then encrypted it
```
ssh-keygen -t rsa
ssh-copy-id -i ~/.shh/id_rsa.pub gary.snap.net.nz
```

# Deploying a new server

## DNS for servers

Put all vm dns entries fully into dns else deployment will fail
[link](https://dnsdb.snap.net.nz)

## LastPass access

LastPass access for adding zeus and root passwords automatically to lastpass
```
env https_proxy="http://frigg.snap.net.nz:3128" lpass login $USER
```

## Virtual machine/s details
export the spreadsheet as a .csv
place the csv in the infra-ansible-server-setup folder

### Generate Hosts script

This creates all the needed files/variables/passwords for the ansible script

```
env https_proxy="http://frigg.snap.net.nz:3128" python generatehosts.py -c filename.csv
```


### Deploy the servers
```
ansible-playbook playbooks/newservers.yml --vault-password-file ./ansible-vault-file -K
```
