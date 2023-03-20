import argparse
import time
import random
import threading

from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.device import ModbusDeviceIdentification


sparse = ModbusSparseDataBlock({20: 0, 40: 0})
base = 35000


def update_value():
    while True:
        v1 = base + 500*random.randint(-4,4)
        v2 = base + 500*random.randint(-4,4)              
        sparse.setValues(20, v1)
        sparse.setValues(40, v2)
        print(str(v1) + " " + str(v2), end='\r')
        time.sleep(5)
        # aggiorna i valori in memoria con set_value

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=False)
    parser.add_argument('--port', type=int, required=False)
    parser.add_argument('--base', type=int, required=False)
    args = parser.parse_args()

    host = args.host
    port = args.port
    base = args.base

    store = ModbusSlaveContext(
            hr = sparse,
            zero_mode=True
        )
    context = ModbusServerContext(slaves=store, single=True)

    #store = ModbusSlaveContext(zero_mode=True)
    #context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName  = 'PyModbus Inc.'
    identity.ProductCode = 'PM'
    identity.VendorUrl   = 'https://github.com/riptideio/pyModbus'
    identity.ProductName = 'Modbus Server'
    identity.ModelName   = 'PyModbus'
    identity.MajorMinorRevision = '1.0'

    if host is None:
        host = '0.0.0.0'

    if port is None:
        port = 8000

    worker = threading.Thread(target=update_value)

    print()
    print("        _____  ______ ___    _____ _____")
    print("       / ___/ / ____//   |  / ___// ___/")
    print("       \__ \ / /    / /| |  \__ \ \__ \ ")
    print("      ___/ // /___ / ___ | ___/ /___/ / ")
    print("     /____/ \__ __/_/  |_|/____//____/  ")
    print("                                        ")
    print("             rogue Modbus server        ")
    print()

    print(" starting memory management thread, base -> {base}".format(base=base))
    worker.start()
    print(" starting Modbus server, {host}:{port}".format(host=host,port=port))
    StartTcpServer(context, identity=identity, address=(host, port))
    print(" stopping Modbus server")
    print(" waiting for the memory management thread to join")
    worker.join()
    