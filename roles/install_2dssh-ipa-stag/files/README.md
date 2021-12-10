# How this works

To make it easy to restrict who can ssh into a server we customize the sshd_config file using `apply_ssh.sh` Therefore if you manually edit sshd_config your changes will be lost when `apply_ssh.sh` is run

:bulb: manually edit the sshd_config file when wanting to set log level to *DEBUG*

## The matches-available folder

Place all your match files here

:bulb: one group/user/address per file

if done via ansible name them **ans_**
if done manually on a server name them **man_**

#### Types of matches

*.address* Match an ip address

*.user* Match a username

*.group* Match a security group

:bulb:for what a match can contain type `man sshd_config`

#### Example

man_intern.user

ans_techm-db.group

ans_davesserver.address




## The matches-enabled folder
:exclamation: **DO NOT** place any files in this folder

instead use the command `sshenmatch` to enable a match rule

instead use the command `sshdismatch` to disable a match rule

`sshenmatch` creates a softlink to the matches-enabled folder

`sshdismatch` removes the softlink from the matches-enabled folder

### Ordering of matches
default server match rules are in the 50 range

:bulb: try to avoid choosing a number under the value of 10 as 10 is reserved for jumphost rules

When enabling a match rule if you want to *"override"* another match rule, make sure the number is lower than the match rule you want to *"override"*

e.g.
the bellow will make it so daves group must use a pubkey

40_allowdavesgroup-pubkeyonly.group
50_allowdavesgroup-password.group

## Applying your changes

run

```bash
apply_ssh.sh
```

`apply_ssh.sh` merges the default `2d.sshd_config` with the matches from the `matches-enabled` folder in the correct order
