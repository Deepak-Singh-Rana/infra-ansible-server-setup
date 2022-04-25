# infra-ansible-server-setup

## Preperation
### Installing Ansible

1. Run the install ansible command as a normal user, this will configure everything you need

    ```
    /usr/local/bin/installansible.sh
    ```
	
2. Log out and log back into the server


### Bitbucket access

1. Set git to use a proxy so we can access bitbucket

    ```
    git config --global http.proxy http://frigg.snap.net.nz:3128
    ```

2. Set yourself a password
on bitbucket go to your settings and generate yourself an "app password" this will be your password when checking out the repo

3. Cloning the repo

    ```
    git clone https://<username>@bitbucket.org/2dgreesdev/infra-ansible-server-setup.git
    ```
    ```
    cd infra-ansible-server-setup
    ```

### Lastpass access

Make sure you have access to the folders

1) `Shared-TechM`

2) `Shared-infra-ansible-server-setup`


### User ssh keys

Make sure you have a rsa ssh key generated and put onto `gary.snap.net.nz:~/.ssh/authorized_keys` so you can authenticate to `gary.snap.net.nz` without a password from the ansible server, else pam_radius config will fail.
```
ssh-keygen -t rsa
```
```
ssh-copy-id -i ~/.ssh/id_rsa.pub gary.snap.net.nz
```

### Required software

```
pip3 install --ignore-installed --user PyYAML pwgen
pip3 install "pyvmomi>=6.7.1.2018.12"
```

#``` do not use
#sudo apt install python3-pyvmomi
#```

```
env https_proxy="http://frigg.snap.net.nz:3128" ansible-galaxy collection install community.vmware
env https_proxy="http://frigg.snap.net.nz:3128" ansible-galaxy collection install community.general
```


# Deploying a new server

:exclamation: Firewall rules, Networking and the domain name to be used, must be complete else deployment will fail:exclamation:

### 0. Firewall rules
[Default rule spreadsheet](https://2degreesnz.sharepoint.com/:x:/r/sites/Team-InfrastructureEngineeringAndOperations/Shared%20Documents/General/Linux/Firewall/new-server-default-firewallrules.xlsx?d=w21b307a19781403f86628d1ba5dfcce9&csf=1&web=1&e=NWrKhi)

### 1. DNS for servers

Put all vm dns entries fully into dns else deployment will fail
[dnsdb link](https://dnsdb.snap.net.nz)

```
cd ~/infra-ansible-server-setup
```

### 2. LastPass access

LastPass access for adding zeus and root passwords/retrieving needed passwords automatically to/from lastpass

```
env https_proxy="http://frigg.snap.net.nz:3128" lpass login --trust $USER

```
### 2.a Update deploy script
```
cd ~/infra-ansible-server-setup
git pull
```


### 3. Virtual machine/s details

* export the spreadsheet as a .csv

* place the csv in the `infra-ansible-server-setup` folder

### 4. Generate Hosts script

This creates all the needed files/variables/passwords for the ansible script

```
env https_proxy="http://frigg.snap.net.nz:3128" python3 generatehosts.py -c filename.csv
```


### 5. Deploy the servers
```
ansible-playbook playbooks/newservers-ipa.yml --vault-password-file tmp/ansible-vault-file
```

