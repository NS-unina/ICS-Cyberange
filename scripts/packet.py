from scapy.all import *
from scapy.layers.inet import *

transaction_id = 2023
protocol_id = 0
length = 6
unit_id = 3

func_code = 6
reference_number = 5
#byte_count = 1                     #da vedere
data = 13000                        #da vedere

class ModbusTCP(Packet):
    name = "mbtcp"
    fields_desc = [ ShortField("Transaction Identifier", transaction_id),
                    ShortField("Protocol Identifier", protocol_id),
                    ShortField("Length", length),                               #da vedere
                    ByteField("Unit Identifier", unit_id)
                    ]

class Modbus(Packet):
    name = "modbus"
    fields_desc = [ XByteField("Function Code", func_code),
                    ShortField("Reference Number", reference_number),
                    ShortField("Data", data)
                    ]
