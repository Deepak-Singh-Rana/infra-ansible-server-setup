# ~/.bash_logout: executed by bash(1) when login shell exits.

# when leaving the console clear the screen to increase privacy

if [ "$SHLVL" = 1 ]; then
    [ -x /usr/bin/clear_console ] && /usr/bin/clear_console -q
fi

#kill off smbnetfs mounts
LASTME=`who |grep $LOGNAME |  wc -l`
if [ "$LASTME" = 1 ]; then
   SMBRUN=`ps -u $LOGNAME | grep smbnetfs | wc -l`
   if [ "$SMBRUN" -ne 0 ]; then
     /bin/fusermount -u $HOME/mnt
     echo killing smbnetfs
   fi
fi
