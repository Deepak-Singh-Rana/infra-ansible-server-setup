#!/usr/bin/perl

my $DEBUG = 1;
my $BackupDir = '/home/homebackups';

@userdir = `/bin/ls /home/`;

foreach my $u (@userdir) {
        chomp $u;

        if($u =~ /\@2degrees.nz/ || $u =~ /\@staff.snap.net.nz/) {


                if(! -e $BackupDir) {
                        `mkdir $BackupDir`;
                        `chmod 700 $BackupDir`;
                }


                my $group;
                ($group) = `/usr/bin/groups $u 2>&1`;

                if($group =~ /no such user/) {
                        chomp $group;
                        print "$u\t\t$group\n" if $DEBUG;

                        my @TarResult = `/bin/tar -czf $BackupDir/$u /home/$u`;
                        `chmod 700 $BackupDir/$u`;
                        print "$u\t\t@TarResult\n\n" if $DEBUG;
                        my @RmResult = `/bin/rm -rf /home/$u`;
                        print "$u\t\t@RmResult\n\n" if $DEBUG;

                }
        }
}
