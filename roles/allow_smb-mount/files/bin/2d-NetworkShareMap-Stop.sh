#!/bin/bash


# set -x


SMBRUN=`ps -u $LOGNAME | grep smbnetfs | wc -l`
if [ "$SMBRUN" -ne 0 ]; then
  /bin/fusermount -u $HOME/mnt
  echo killing smbnetfs
fi
