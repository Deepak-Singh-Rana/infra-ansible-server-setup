#!/usr/bin/python3
import os
import subprocess
import glob

clamavdir="/etc/clamav"
confddir="/etc/clamav/2d-conf.d/"
scanlist="2d-scanlist.conf"
scanlistcommand="--file-list="+clamavdir+"/"+scanlist
excludelist="/etc/clamav/2d-excludelist.conf"
logfile="/tmp/clamav-$(date +'%Y-%m-%d').log";

excludedirs=""
includedirs=""

#cd to the conf.d folder
os.chdir(confddir)
#build the exlude list
for file in glob.glob("*.exclude"):

        print("opening: " + file)
        file = open(file, 'r')
        lines = file.readlines()

        for line in lines:
                line = line.replace("\n", "")
                print(line)
                excludedirs += ("--exclude="+line+" ")

#build the include list
for file in glob.glob("*.include"):
        print("opening: " + file)
        file = open(file, 'r')
        lines = file.readlines()

        for line in lines:
                line = line.replace("\n", "")
#               includedirs += ("--include-dir=\""+line+"\" ")
                includedirs += (line+"/\n")

toscan = open(clamavdir+"/"+scanlist, 'w')
toscan.writelines(includedirs)
toscan.close()

#print("excluded dirs: "+excludedirs)
#print("included dirs: "+includedirs)
os.chdir("/")

#print(excludedirs+"\n")
#print(scanlistcommand+"\n")

#build our clamav script that includes our excluded and included dirs
runcommand = open("/usr/local/sbin/clamav.sh", 'w')
os.chmod("/usr/local/sbin/clamav.sh", 0o700)
runcommand.write("#!/bin/bash\n")
runcommand.write("freshclam\n")
runcommand.write("ionice -c3 nice -n 19 /usr/bin/clamscan -riv --scan-elf=yes "+excludedirs+" "+scanlistcommand+"\n")
runcommand.close()

#update the clamav database
subprocess.run(["/usr/local/sbin/clamav.sh"])
#run a scan using our updated clamav script
subprocess.run(["/usr/local/sbin/clamav.sh"])

#ionice -c3 nice -n 19 /usr/bin/clamscan -ri --scan-elf=yes --file-list=$IncludeConf | tee "$LogFile";
