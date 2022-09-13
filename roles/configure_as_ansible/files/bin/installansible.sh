#!/bin/bash
if [[ $EUID -ne 0 ]]; then
	#set the proxy so we can reach pip repos
	export http_proxy=http://frigg.snap.net.nz:3128
	export https_proxy=http://frigg.snap.net.nz:3128

	#below is done as the current user
	#update pip
	python3 -m pip install -U pip
	#install require package
	python3 -m pip install --user setuptools_rust
	#install ansible
	python3 -m pip install --user ansible
        #install pwgen
        python3 -m pip install --ignore-installed --user PyYAML pwgen
        #install pyvmomi
        python3 -m pip install "pyvmomi>=6.7.1.2018.12"

	#set execuatble permissions on ansible files
	chmod 700 ~/.local/bin/ansible*

	if grep -Fxq "alias ap=~/.local/bin/ansible-playbook" ~/.bashrc
	then
		echo "ap alias to ansible-playbook already found"
	else
		echo "creating shortcut to ansible-play as 'ap'"
		echo "alias ap=~/.local/bin/ansible-playbook" >> ~/.bashrc
	fi


        echo "please log out and log back in for ansible to become available"
else
	echo "This script must not be run as root" 
	exit 1
fi
