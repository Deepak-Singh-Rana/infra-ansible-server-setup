#template deploy pre-requirement
you must deploy the ansible-deploy.pub cert to your new template before you 
can run ansible scripts against it as ansible uses the key to log in (no password)

ssh-copy-id -i ./ansible-deploy.key zeus@202.37.101.219