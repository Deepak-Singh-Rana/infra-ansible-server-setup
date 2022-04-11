#!/usr/bin/perl

my $DEBUG = 1;
my $BackupDir = '/home/homebackups';

@userdir = `/bin/ls /home/`;

foreach my $u (@userdir) {
        chomp $u;

#       print "all users in /home: $u\n";
        #grab users with mgt appended to thier name
        if($u =~ /mgt./) {

                print "mgt user: $u\n";
                #make backup dir if it doesn't exist
                if(! -e $BackupDir) {
                        `mkdir $BackupDir`;
                        `chmod 700 $BackupDir`;
                }

                # get the group of the current user we are dealing with
                my $group;
                ($group) = `/usr/bin/groups $u 2>&1`;
                print "$group\n";

                #if searching the group shows "no such user"
                if($group =~ /no such user/) {
                        chomp $group;
                        print "$u\t\t$group\n" if $DEBUG;

                        #tar up thier home folder
                        my @TarResult = `/bin/tar -czf $BackupDir/$u /home/$u`;
                        `chmod 700 $BackupDir/$u`;
                        print "$u\t\t@TarResult\n\n" if $DEBUG;

                        #then delete their old home folder
                        my @RmResult = `/bin/rm -rf /home/$u`;
                        print "$u\t\t@RmResult\n\n" if $DEBUG;

                }
        }
}

