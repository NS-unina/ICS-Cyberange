from scapy.all import *
from scapy.layers.inet import *

from random import randint

#byte_count = 1                     #da vedere
#data = 13000
#transaction_id = 2023
#protocol_id = 0
#length = 6
#unit_id = 3

#func_code = 6
#reference_number = 5
#data = 10000


class ModbusTCP(Packet):

    name = 'mbtcp'

    fields_desc = []
                 # ShortField('Transaction Identifier', transaction_id),
                 # ShortField('Protocol Identifier', protocol_id),
                 # ShortField('Length', length),                               #da vedere
                 # ByteField('Unit Identifier', unit_id)
                 #   ]

    def __init__(self):
        self.fields_desc.append(ShortField('Transaction Identifier', 2023))
        self.fields_desc.append(ShortField('Protocol Identifier', 0))
        self.fields_desc.append(ShortField('Length', 6))
        self.fields_desc.append(ByteField('Unit Identifier', 2))

class Modbus(Packet):

    name = 'modbus'
    
    fields_desc = [] 
                #   XByteField('Function Code', func_code),
                #   ShortField('Reference Number', reference_number),
                #   ShortField('Data', data)
                #    ]

    def __init__(self):
        self.fields_desc.append(XByteField('Function Code', 6))
        self.fields_desc.append(ShortField('Reference Number', 5))
        self.fields_desc.append(ShortField('Data', 10000))
