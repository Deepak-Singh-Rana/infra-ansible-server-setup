# td-ansible-server-setup
2degrees linux ansible repo

for all linux servers

## BITBUCKET info

### preparing for intial checkout

#### Set git to use a proxy so we can access bitbucket
git config --global http.proxy http://frigg.snap.net.nz:3128

#### Set yourself a password
on bitbucket go to your settings and generate yourself an "app password" this will be your password when checking out the repo


### checking out the repo

```

$git clone https://<username>@bitbucket.org/2dgreesdev/td-ansible-server-setup.git

```

## How to push your changes

```
$ git add .

$ git commit -m "comment about your changes here"

$ git push

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
ansible-galaxy collection install community.vmware

##### ansible-vault-passwords file
to create/encrypt/decrypt the file, you use:

for new file:

ansible-vault create testfile.txt --vault-password-file=ansible-vault-file

for encrypting existing file:

ansible-vault encrypt testfile.txt --vault-password-file=ansible-vault-file

for decrypting:

ansible-vault decrypt testfile.txt --vault-password-file=ansible-vault-file

when executing the above, you will notice it doesn't ask for password.


# Deploying a new server

## Fill out the vmcenter details
```
nano vars/newserver_vcenterdetails.yml
```

### Ubuntu 18
```
nano vars/newserver_ubuntu18.yml
ansible-playbook playbooks/newserver_ubuntu18.yml --vault-password-file ./ansible-vault-file
```
### Redhat 8
```
nano vars/newserver_rhel8.yml
ansible-playbook playbooks/newserver_redhat8.yml --vault-password-file ./ansible-vault-file
```


