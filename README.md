# oh3node
OH3SPN Packet Node

This is very much in testing status and currrently does little of any use.

We don't talk ax.25 so this should be called using axwrapper via ax25d.

Example ax25d.conf file:-

[OH3SPN-7 VIA hf]
default  * * * * * *  - username  /usr/sbin/axwrapper axwrapper /home/username/git/oh3node/oh3node.py oh3node.py
parameters_extAX25 VC-disc-on-linkfailure-msg VC-log-connections

