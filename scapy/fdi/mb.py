from scapy.all import *
from scapy.layers.inet import *

from random import randint


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
