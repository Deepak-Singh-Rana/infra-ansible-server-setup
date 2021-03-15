# Firewall package INFO

## how to apply the rules
to apply the enabled rules type
```bash

firewall-up

```

to disabble the firewall type
```bash

firewall-down

```

## enabled rules are applied on boot
the firewall applys enabled rules on boot via NetworkManager dispatch.d


## example-rules

This contains examples of how to setup firewall rules

## rules-available

This folder is where you put your rules for single servers
use the file extension *.v4* for **IPv4**, *.v6* for **IPv6**, and *.ipset* for **IP set** so the firewall script knows which IP the rules are for

Use the format man_protocolname-detail.v4/.v6

:exclamation: Do not edit *ans_* or *pkg_* rules as they will automatically get overwritten when the playbook/package that created them gets updated


## rules-enabled

:exclamation:Do not manually put anything in this folder
Use the below options instead 
*enable a rule*
```bash

fwenrule

```
*disable a rule*
```bash

fwdisrule

```
*move rules around*
```bash

fwmvrule

```
## networks
:exclamation: Do not modify the base rules in this folder, they will be overwritten when the pacakge is updated


##custom_networks.d
put any custom networks in here
