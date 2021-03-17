# How this works

## matches-available folder
Place all your files here

if done via ansible name them *ans_*
if done manually on a server name them *man_*

## types of matches
*.address* Match an ip address

*.user* Match a username

*.group* Match a security group

#### manually created example
man_techm-dbops.group

#### Ansible example
ans_techm-ops.group


## matches-enabled folder
:exclamation: **DO NOT** place any files in this folder

instead use the command `sshenmatch` to enable a match rule
instead use the command `sshdismatch` to disable a match rule

only have one security group per .group file
