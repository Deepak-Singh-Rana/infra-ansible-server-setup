# Firewall package INFO
## rules-available

these folders are where you put your rules and network aliases for single servers
use the file extension *.v4* for **IPv4** and *.v6* for **IPv6** so the firewall script knows which IP the rules are for

Use the format man_protocolname-detail.v4/.v6



## rules-enabled

:exclamation:Do not put anything in this folder
Use the below options instead 
enable a rule
```bash
fwenrule
```
disable a rule
```bash
fwdisrule
```
move rules around
```bash
fwmvrule
```
## networks
:exclamation: Do not modify the base rules in this folder, they will be overwritten when the pacakge is updated
