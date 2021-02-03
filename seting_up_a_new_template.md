preparing a template

##copy the ssh key
ssh-copy-id -i ansible-deploy.key.pub zeus@202.37.101.219

##configure sshd_config to allow logins with just "publickey"
nano /etc/ssh/sshd_config

##allow zeus to sudo without password /etc/sudoers.d/deploy_zeus#this file should not exist on live servers,
#this file should not exist on live servers, it's used for deployment of the template only
zeus	ALL=(ALL) NOPASSWORD:ALL

redhat to fix


###tofix


TASK [base_role : Redhat satellite check repo https://snzclakl173.nzc.co.nz is accessable] *****************************
fatal: [redhat8-ansdeployment.snap.net.nz]: FAILED! => {"changed": false, "elapsed": 10, "msg": "Status code was -1 and not [200]: Request failed: <urlopen error timed out>", "redirected": false, "status": -1, "url": "https://snzclakl173.nzc.co.nz"}
...ignoring


172.21.238.9	ak01vvmpe007	80/tcp,443/tcp,8000/tcp,5000/tcp,5647/tcp,8140/tcp,8443/tcp,9090/tcp
172.23.238.9	hn02vvmpe007	80/tcp,443/tcp,8000/tcp,5000/tcp,5647/tcp,8140/tcp,8443/tcp,9090/tcp
