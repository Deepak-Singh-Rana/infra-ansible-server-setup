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
for file in glob.glob("*.exclude"):

        print("opening: " + file)
        file = open(file, 'r')
        lines = file.readlines()

        for line in lines:
                line = line.replace("\n", "")
                print(line)
                excludedirs += ("--exclude="+line+" ")

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

print(excludedirs)
print(includedirs)
os.chdir("/")
#exit(0)
#subprocess.run(["ionice", "-c3", "nice", "-n", "19", "/usr/bin/clamscan", "-riv", "--scan-elf=yes", excludedirs, scanlistcommand, "|", "tee", logfile])
#print("/usr/bin/clamscan -riv --scan-elf=yes "+ excludedirs+" "+includedirs)
#print("/usr/bin/clamscan -riv --scan-elf=yes "+scanlistcommand)
#subprocess.run(["/usr/bin/clamscan", "-riv", "--scan-elf=yes", excludedirs, includedirs])
print(excludedirs+"\n")
print(scanlistcommand+"\n")
runcommand = open("/usr/local/sbin/clamav.sh", 'w')
os.chmod("/usr/local/sbin/clamav.sh", 0o700)
runcommand.write("#!/bin/bash\n")
runcommand.write("/usr/bin/clamscan -riv "+excludedirs+" "+scanlistcommand+"\n")
runcommand.close()
subprocess.run(["/usr/local/sbin/clamav.sh"])

#ionice -c3 nice -n 19 /usr/bin/clamscan -ri --scan-elf=yes --file-list=$IncludeConf | tee "$LogFile";
