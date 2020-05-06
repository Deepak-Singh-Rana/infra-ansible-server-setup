#!/usr/bin/perl

#Check for the existance of the program pwgen
my @a = `which pwgen`;
if(!@a) {print "ERROR: pwgen not found in path\napt-get install pwgen\n"; exit; }

#make sure we are running as root
my @a = `whoami`;
if($a[0] !~ /root/) {print "ERROR: not root, must be root\n"; exit; }


######################
#List of users

@usernames = ('root','zeus');

foreach my $user (@usernames) {

        my %Password = &MakePassword();
        my $result = &SetPassword($user,$Password{'crypt'});
	#print [BG]-<user>-<FQDN>     <user>      <password>
	#e.g. [BG]-zeus-deathstar     zeus        fakePaSSW0Rd
        print "[BG]-$user-$ENV{HOSTNAME}\t$user\t$Password{'cleartext'}\n";

}

######################


#generate the new password
sub MakePassword(){

        my %Pass;
        $Pass{'salt'} = chr(65+rand(27)).chr(65+rand(27)).chr(65+rand(27)).chr(65+rand(27)).chr(65+rand(27)).chr(65+rand(27)).chr(65+rand(27)).chr(65+rand(27));         $Pass{'cleartext'} = `pwgen -B -N 2`;
        $Pass{'cleartext'} =~ s/\s//g;
        $Pass{'crypt'} = crypt($Pass{'cleartext'} , "\$6\$$Pass{'salt'}\$");

        return %Pass;
}

#change the password
sub SetPassword(){

        my $user = shift;
        my $pass = shift;

        open OUT, '|chpasswd -e' or die "can't open pipe: chpasswd $!";
        print OUT "$user:$pass";
        close OUT

}
