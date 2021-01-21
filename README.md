# td-ansible-server-setup
2degrees linux ansible repo
for all linux servers
https://bitbucket.org/2dgreesdev/td-ansible-server-setup/src/master/README.md 

## BITBUCKET info

### preparing for intial checkout

#### Set git to use a proxy so we can access bitbucket
git config --global http.proxy http://frigg.snap.net.nz:3128

#### Set yourself a password
on bitbucket go to your settings and generate yourself an "app password" this will be your password when checking out the repo


### checking out the repo

```

git clone https://<username>@bitbucket.org/2dgreesdev/td-ansible-server-setup.git

```

## How to push your changes

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


# Deploying a new server

##make sure you have created a personal.yml file from personal.yml.example and then encrypted it
```
cp personal.yml.example personal.yml
nano personal.yml
ansible-vault encrypt personal.yml --vault-password-file=ansible-vault-file
```

## User ssh keys
make sure you have a rsa ssh key generated and put onto gary so you can authenticate to gary without a password, else pam_radius config will fail

## DNS for servers
put all vm dns entries fully into dns else deployment will fail

## Fill out the vmcenter details
```
nano vars/newserver_vcenterdetails.yml
```
copy from vars/newserver_vcenterdetails.yml.example if need be

## Virtual machine/s details
in vm_vars put all the details of each server you want to build into a .yml file  
The filename for each vm should be fqdn.yml  
_e.g._  
_ubuntu18server.snap.net.nz.yml_  
_redhat8server.2d.nz.yml_  




### Ubuntu 18
```
ansible-playbook playbooks/newservers.yml --vault-password-file ./ansible-vault-file
```
~~### Redhat 8~~
```
ansible-playbook playbooks/newservers.yml --vault-password-file ./ansible-vault-file
```

### after deployment
reboot server, then log in using your AD account
```
set-root-password.pl
```
then put the root passwords into the breakglass folder in lastpass

