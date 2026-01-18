
from micropython import const
import struct


_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_MAX_PAYLOAD = const(31)

_voltage = const(0xfc)
_temperature = const(0xfe)
_pico_id = (0xfd)



# Generate a payload to be passed to gap_advertise(adv_data=...).
def advertising_payload(voltage=0, temperature=0):
    payload = bytearray()
    flags = struct.pack("B", 0x01)
    payload += struct.pack("BB", 2, _ADV_TYPE_FLAGS) + flags
    
    # Add name
    name = "Pico"
    payload += struct.pack("BB", len(name)+1, _ADV_TYPE_NAME) + name

    # Add pico ID
    id = bytearray()
    id.append(4)
    payload += struct.pack("BB", len(id)+1, _pico_id) + id

    # Add the voltage
    voltage = round(voltage, 2)
    print(voltage)
    b = bytearray()
    v = int(voltage)
    mv = int((voltage-v)*100)
    b.append(v)
    b.append(mv)
    payload += struct.pack("BB", len(b)+1, _voltage) + b
    
    # Add the temprature
    t = float(temperature)
    deg = int(t)
    deg2 = int((t-deg)*100)
    tempbytes = bytearray()
    tempbytes.append(deg)
    tempbytes.append(deg2)
    payload += struct.pack("BB", len(tempbytes)+1, _temperature) + tempbytes

    if len(payload) > _ADV_MAX_PAYLOAD:
        raise ValueError("advertising payload too large")
    print(payload)
    return payload




