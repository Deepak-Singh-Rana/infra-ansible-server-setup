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


### Required software

```
pip3 install --ignore-installed --user PyYAML pwgen onepasswordconnectsdk
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

### 1 Update deploy script
```
cd ~/infra-ansible-server-setup
git pull
```

### 2. Virtual machine/s details

* export the spreadsheet as a .csv

* place the csv in the `infra-ansible-server-setup` folder

### 3. Generate Hosts script

This creates all the needed files/variables/passwords for the ansible script

```
./generatehosts
```


### 4. Deploy the servers
```
ansible-playbook playbooks/newservers-2dl.nz.yml --vault-password-file tmp/ansible-vault-file
```

### 5. Ubuntu join landscape
If it's an ubuntu server browse to "https://landscape.2degrees.nz" and accept your recently deployed servers request to join landscape
