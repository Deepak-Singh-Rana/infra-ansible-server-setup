#!/bin/bash
#passowrd is truely random, no ambigus chars 16 in length and 1 password
password=`pwgen -s -B 16 1`
sed -i "s/^\([^ ]*\)[ ]*\(.*\)\([ ][0-9]\)/\1 ${password}\3/g" /etc/pam_radius_auth.conf
ipv6=`ip -6 addr show scope global | awk '$1 == "inet6" {print $2}' | cut -d"/" -f 1`
ipv4=`ip -4 addr show scope global | awk '$1 == "inet" {print $2}' | cut -d"/" -f 1`
#echo "$ipv4" | cut -d"/" -f 1
echo "Secrets added to file"
tput setaf 3
echo "Run the following on gary and lary to add the details into radius"
tput sgr0
echo "rad_client_add -i $ipv4 -s $password -h $HOSTNAME"
echo "rad_client_add -i $ipv6 -s $password -h $HOSTNAME"
