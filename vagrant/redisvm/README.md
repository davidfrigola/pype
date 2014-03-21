
# Vagrant VM definition

# Requisites
Vagrant 1.4.3

# Commands on VM
Start $ vagrant up
Stop $ vagrant halt
Connect to $ vagrant ssh

# VM config details
IP public 192.168.10.10
Redis port forwarded from host (default REDIS port 6379)

# Usefull stuff
You can connect vía telnet to REDIS
telnet localhost 6379
(This is possible -via localhost - due port forwarding)