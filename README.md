# td-ansible-server-setup


2degrees linux ansible repo

for all linux servers

##How to checkout the repo

###preparing for intial checkout

####Set git to use a proxy so we can access bitbucket
git config --global http.proxy http://frigg.snap.net.nz:3128

####Set yourself a password
on bitbucket go to your settings and generate yourself an "app password" this will be your password when checking out the repo

```

###checking out the repo

```

$git clone https://<username>@bitbucket.org/2dgreesdev/td-ansible-server-setup.git

```

##How to push your changes

```
$ git add .

$ git commit -m "comment about your changes here"

$ git push

```

#setting up a new server

$ ansible-playbook playbooks/newserver-ubuntu18.yml --ask-vault-pass
$ ansible-playbook playbooks/newserver-redhat8.yml

####updating ansible-galaxy roles
export http_proxy=http://frigg.snap.net.nz:3128
export https_proxy=https://frigg.snap.net.nz:3128

ansible-galaxy collection install community.****
#####e.g.
ansible-galaxy collection install community.vmware



##### ansilbe-vault-passwords file
you need to create the vault password file first, here is how:

openssl rand -base64 512 |xargs > vaultkeyfile

i am creating the vault file at local directory, but probably you want to place it to another one, like ~/.ansible_vault/ for example.

then to create/encrypt/decrypt the file, you use:

for new file:

ansible-vault create testfile.txt --vault-password-file=vaultkeyfile

for encrypting existing file:

ansible-vault encrypt testfile.txt --vault-password-file=vaultkeyfile

for decrypting:

ansible-vault decrypt testfile.txt --vault-password-file=vaultkeyfile

when executing the above, you will notice it doesn't ask for password.
