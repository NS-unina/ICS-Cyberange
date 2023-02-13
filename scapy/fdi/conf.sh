#!/bin/bash

ip link add link eth1 name eth2 address 22:7e:b8:51:c0:76 type macvlan
ip link add link eth1 name eth3 address 80:df:21:89:62:22 type macvlan
ip link set dev eth2 up
ip link set dev eth3 up
ip addr add 10.0.0.211/24 dev eth2
ip addr add 10.0.0.212/24 dev eth3
sysctl -w net.ipv4.ip_forward=1
