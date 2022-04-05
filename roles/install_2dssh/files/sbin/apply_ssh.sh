#!/bin/bash

# ssh_apply.sh, what i do is append the /etc/ssh/sshd_config.d/matches file onto the end of /etc/ssh/sshd_config
# I get run by the 2d-ssh package and manually after to apply manuall changes to the matches file
#

sshdconfig_file="/etc/ssh/sshd_config"
sshddefault_file="/etc/ssh/2d.sshd_config"
matches="/etc/ssh/matches-enabled"

echo "generating sshd_config file..."

#build the sshd file
cat $sshddefault_file $matches/*.conf $matches/*.address $matches/*.user $matches/*.group > $sshdconfig_file

#make sure permissions are correct
echo "setting permissions to sshd_config..."
chown root:root ${sshdconfig_file}
chmod 400 ${sshdconfig_file}
echo "restarting sshd..."
systemctl restart sshd
