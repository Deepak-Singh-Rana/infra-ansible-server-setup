# td-ansible-server-setup


2degrees linux ansible repo

for all linux servers

##How to checkout the repo

###preparing for intial checkout

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
