#!/bin/bash

# ssh_apply.sh, what i do is append the /etc/ssh/sshd_config.d/matches file onto the end of /etc/ssh/sshd_config
# I get run by the 2d-ssh package and manually after to apply manuall changes to the matches file
#

sshdconfig_file="/etc/ssh/sshd_config"
sshddefault_file="/etc/ssh/2d.sshd_config"
matches="/etc/ssh/sshd_config.d/matches"

echo "generating sshd_config file..."
if [ ! -f ${matches} ]
then
        echo "no matches file found, not appending to sshd_config..."
        cat $sshddefault_file > $sshdconfig_file
else
        cat $sshddefault_file $matches > $sshdconfig_file
fi
#make sure permissions are correct
echo "setting permissions to sshd_config..."
chown root:root ${sshdconfig_file}
chmod 400 ${sshdconfig_file}
echo "restarting sshd..."
systemctl restart sshd
