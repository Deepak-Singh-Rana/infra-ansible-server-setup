#cron runs daily checks and compares /var/lib/aide/aide.db.new to /var/lib/aide/aide.db
#the cron job is run at 5am, so has already run for today so we wont need the aide.db file anymore

OS=`awk -F= '/^NAME/{print $2}' /etc/os-release`
echo $OS


###############################
## Rsync needed files offbox ##
###############################
DAY=`date +%Y%m%d`
echo $OS
case $OS in

        '"Red Hat Enterprise Linux"')
        #cp last nights database build(aide.db.new) to aide.db
        #####################################################
        ## cp the old database to be readyt for comparison ##
        #####################################################
        cp /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz

        ############################
        ## build the new database ##
        ############################
        aide --init

        DAYDPKG=dnf.log.$DAY
        DAYAIDE=aide.db.$DAY
        cp /var/lib/aide/aide.db.new.gz /tmp/$DAYAIDE
        cp /var/log/dnf.log /tmp/$DAYDPKG

        ;;

        '"Ubuntu"')
        #cp last nights database build(aide.db.new) to aide.db
        #####################################################
        ## cp the old database to be readyt for comparison ##
        #####################################################
        cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db

        ############################
        ## build the new database ##
        ############################
        aideinit -f

        DAYDPKG=dpkg.log.$DAY
        DAYAIDE=aide.db.$DAY
        cp /var/lib/aide/aide.db.new /tmp/$DAYAIDE
        cp /var/log/dpkg.log /tmp/$DAYDPKG

        ;;
esac
export RSYNC_PASSWORD=SDF567GFHJ4356rte
#Copy over the two files that the aide filesystem monitoring script need to spot changes in the filesystem
rsync /tmp/$DAYAIDE aidedatabases@splunkforwarder01.snap.net.nz::aidestorage/$HOSTNAME/
rsync /tmp/$DAYDPKG aidedatabases@splunkforwarder01.snap.net.nz::aidestorage/$HOSTNAME/
rm /tmp/$DAYAIDE
rm /tmp/$DAYDPKG
