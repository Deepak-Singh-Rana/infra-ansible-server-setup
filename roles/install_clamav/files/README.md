## 2d clamav

the systemd service '2d-clamav.service' runs clamav.py
clamav.py will run `freshclam` do update the clamav database, then oraganise included and excluded dirs and then build a clamav.sh script, then run the script

if you want a folder/file excluded you can put it in the '/etc/clamav/2d-conf.d' folder
if it's in an ansible role name it 
##_ans_*.exclude
##_ans_*.include

if it's manually made on the server name it
##_man_*.exclude
##_man_*.include

