from datetime import datetime
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

scanner = Scanner().withDelegate(ScanDelegate())

# Scan for BLE devices for 10 seconds
while True:
    print("scanning...")
    try:
        devices = scanner.scan(10.0, passive=True)
    except:
        continue

    for dev in devices:
       # print(dev.addr)

        if any(desc == "Complete Local Name" and value == "Pico" for (_, desc, value) in dev.getScanData()):
            print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
            id = 0
            voltage = 0
            temperature = 0

            for (adtype, desc, value) in dev.getScanData():
                #print("%s  %s = %s" % (adtype, desc, value))
                if adtype == 253:
                    id = value
                if adtype == 252:
                    #print(value)
                    v = int(value[:-2], 16)
                    mv = int(value[-2:], 16)
                    if mv <= 9 and value[2] == "0":
                        mv = str(mv).zfill(2)
                    voltage = str(v) + "." + str(mv)

                if adtype == 254:
                    deg = int(value[:-2], 16)
                    deg2 = int(value[-2:], 16)
                    if deg2 <= 9 and value[2] =="0":
                        deg2 = str(deg2).zfill(2)
                    temperature = str(deg) + "." + str(deg2)
                t = datetime.now()

            with open("/var/www/output.csv", "a+") as f:
                f.write(str(t) + ", " + str(id) + ", " + str(voltage) + ", " + str(temperature) + "\n")
            print("Found a beacon at " + str(t))

