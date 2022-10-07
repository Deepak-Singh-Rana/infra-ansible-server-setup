#!/bin/bash

# set -x

ERROR=0
CONFDIR="$HOME/.smb"
DATADIR="$HOME/mnt"

echo
#check for conf dir
if [ -d "$CONFDIR" -a ! -h "$CONFDIR" ]
then
        echo "Configuration Directory $CONFDIR exist.. good"
else
        echo "Configuration Directory $CONFDIR does not exist.. bad. see Admin"
        ERROR=1
fi

#check for the mnt dir
if [ -d "$DATADIR" -a ! -h "$DATADIR" ]
then
        echo "Data Directory $DATADIR exist.. good"
else
        echo "Data Directory $datedir does not exist.. bad. see Admin"
        ERROR=1
fi

if [ "$ERROR" == "1" ]
then
        echo "Exiting with Errors"
        exit
fi

AUTH=`grep -cP ^auth $CONFDIR/smbnetfs.auth`
if [ "$AUTH" == "0" ]
then
        echo "No Authencation configurtion found in $CONFDIR/smbnetfs.auth Please edit"
        ERROR=1
fi

HOST=`grep -cP ^link $CONFDIR/smbnetfs.host`
if [ "$HOST" == "0" ]
then
        echo "No Host configurtion found in $CONFDIR/smbnetfs.host Please edit"
        ERROR=1
fi

if [ "$ERROR" == "1" ]
then
        echo "Existing with Errors"
        exit
fi

echo "Looks good, mounting remote smb share. 'cd $DATADIR' to see your mounted shares"
echo

/usr/bin/smbnetfs $DATADIR
