import argparse

from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, required=False)
parser.add_argument('--port', type=int, required=False)
args = parser.parse_args()

host = args.host
port = args.port

store = ModbusSlaveContext(
        hr = ModbusSequentialDataBlock(40030, [35000]),
        zero_mode=True
    )
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName  = 'PyModbus Inc.'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'https://github.com/riptideio/pyModbus'
identity.ProductName = 'Modbus Server'
identity.ModelName   = 'PyModbus'
identity.MajorMinorRevision = '1.0'

if host is None and port is None:
    host = '127.0.0.1'
    port = 8000

print("Avvio server Modbus, {host}:{port}".format(host=host,port=port))
StartTcpServer(context, identity=identity, address=(host, port))
print("Chiusura server Modbus")
