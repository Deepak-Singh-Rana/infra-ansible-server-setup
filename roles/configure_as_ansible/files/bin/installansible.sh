#!/bin/bash
if [[ $EUID -ne 0 ]]; then
	#set the proxy so we can reach pip repos
	export http_proxy=http://frigg.snap.net.nz:3128
	export https_proxy=http://frigg.snap.net.nz:3128

	#below is done as the current user
	#update pip
	python3 -m pip install -U pip
	#isntall require package
	python3 -m pip install --user setuptools_rust
	#isntall ansible
	python3 -m pip install --user ansible

	#set execuatble permissions on ansible files
	chmod 700 ~/.local/bin/ansible*

        echo "please log out and log back in for ansible to become available"
else
	echo "This script must not be run as root" 
	exit 1
fi
