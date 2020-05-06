#!/bin/bash
#checks when certs expire
####Note* there is a simmilar script in the 2d-ca package####
#######which check whether certs on the ca will expire#######
expiretime="90"
#search the filesystem for files ending in .crt or pem

#check for snap.net.nz certs
readarray -t certs < <(mlocate .snap.net.nz. | egrep "crt|pem")
for cert in "${certs[@]}"
do
        #echo "checking $cert"
        ssl-cert-check -a -E $HOSTNAME@snap.net.nz -e sysadmin@2degrees.nz -c $cert -x $expiretime
done

#cleanup for next run
unset certs
unset cert

#check for 2degrees.nz certs
readarray -t certs < <(mlocate .2degrees.nz. | egrep "crt|pem")
for cert in "${certs[@]}"
do
        #echo "checking $cert"
        ssl-cert-check -a -E $HOSTNAME@snap.net.nz -e sysadmin@2degrees.nz -c $cert -x $expiretime
done

#cleanup for next run
unset certs
unset cert
