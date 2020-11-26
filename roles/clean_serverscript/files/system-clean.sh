#!/bin/bash
######################
##  Server Refresh? ##
######################
function function_cleanupos () {
        #cleanup script for fresh ubuntu/redhat deployments from templates

        #stop rsyslog for cleaning up the logs
        echo "stopping rsyslog"
        systemctl stop rsyslog

	#create new machine-id
	rm /etc/machine-id
	systemd-machine-id-setup

        #clear audit logs
        if [ -f /var/log/audit/audit.log ]; then
            echo "cleaning audit.log"
            cat /dev/null > /var/log/audit/audit.log
        fi
        if [ -f /var/log/wtmp ]; then
            echo "cleaning wtmp"
            cat /dev/null > /var/log/wtmp
        fi
        if [ -f /var/log/lastlog ]; then
            echo "cleaning lastlog"
            cat /dev/null > /var/log/lastlog
        fi

        #cleanup persistent udev rules
            echo "cleaning /etc/udev/rules.d/70-persistent-ipoib.rules"
        if [ -f /etc/udev/rules.d/70-persistent-ipoib.rules ]; then
            rm /etc/udev/rules.d/70-persistent-ipoib.rules
        fi

        #clean  tmp dirs
        echo "removing contents of /tmp/ and /var/tmp/"
        rm -rf /tmp/*
        rm -rf /var/tmp/*

        #clean ssh keys
        echo "regenerating ssh keys"
	#if our signed hostkey exist don't delete the ed25519 host keys
        if [ -f /etc/ssh/ssh_host_ed25519_key-cert.pub ]; then
	        rm -f /etc/ssh/ssh_host_rsa*
	        rm -f /etc/ssh/ssh_host_ecdsa*
	else
	#remove all the host keys
	        rm -f /etc/ssh/ssh_host_*
        fi
        #add check for ssh keys on reboot...regenerate if neccessary
        ssh-keygen -t rsa -N "" -f /etc/ssh/ssh_host_rsa_key
        ssh-keygen -t ecdsa -N "" -f /etc/ssh/ssh_host_ecdsa_key
	#if our signed host key does not exist then generate a new ed25519 host key
        if [ ! -f /etc/ssh/ssh_host_ed25519_key-cert.pub ]; then
             ssh-keygen -t ed25519 -N "" -f /etc/ssh/ssh_host_ed25519_key
        fi

        #clean apt
        if [ -f "/usr/bin/apt" ]; then
                echo " cleaning apt"
                apt clean
        fi
        if [ -f "/usr/bin/dnf" ]; then
                echo " cleaning dnf"
                dnf clean all
        elif [ -f /usr/bin/yum/ ]; then
            echo " cleaning yum"
            yum clean all
        fi
        #clean history
        echo "cleaning history"
        history -c
        history -w

        echo "removing old journalctl logs"
        journalctl --vacuum-time=1d

        #start rsyslog
        echo "starting rsyslog"
        systemctl start rsyslog


        echo ""
        echo "--------------------------------------------------------------"
        echo "You must now restart the system for the changes to take effect"
}
#check to see if we passed a "y" argument to skip the questions
echo "$1"
if [[ $1 == "y" ]]; then
        function_cleanupos
else
        echo "---------------"
        echo "Do you want to run the refresh scripts?"
        tput setaf 1
        echo "!!WARNING this will reset sshd/wipe the CA cert and wipe things like logs!!"
        tput sgr0
        echo ""
        WIPECHOICE=false
        while [ $WIPECHOICE == "false" ]
        do
                tput setaf 3
                read -r -p $'[w]Wipe | [d]Dont wipe | [q]Quit\n' response
                tput sgr0
                #the below forces it to be lowercase
                wiperesponse=${response,,}
                if [[ "$wiperesponse" =~ ^[d]$ ]]; then
                        echo "script complete"
                        exit 1;
                elif [[ "$wiperesponse" =~ ^[q]$ ]]; then
                        echo "user chose to quit"
                        WIPECHOICE=true
                elif [[ "$wiperesponse" =~ ^[w]$ ]]; then
                        WIPECHOICE=true
                        tput setaf 3
                        read -r -p $'Are you sure you want to reset ssh/wipe the CA cert and things like logs? y/N | [q]Quit\n' sureresponse
                        tput sgr0
                        doublesureresponse=${sureresponse,,}
                        if [[ "$doublesureresponse" =~ ^[n]$ ]]; then
                                echo "not wiping, script complete"
                                exit 1;
                        elif [[ "$doublesureresponse" =~ ^[q]$ ]]; then
                                echo "ueer choese to quite, not wiping, script complete"
                                exit 1;
                        elif [[ "$doublesureresponse" =~ ^[y]$ ]]; then
                                function_cleanupos
                        fi
                else
                        echo "not wiping, script complete"
                fi
        done
fi
