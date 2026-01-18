
import bluetooth
import time
import machine
from ble_advertising import advertising_payload
import onewire
import ds18x20
import network


class BLETemperature:
    def __init__(self, ble, voltage, temperature, name=""):
        
        self._ble = ble
        self._ble.active(True)
        self._payload = advertising_payload(voltage=voltage, temperature=temperature)
        self._advertise()

    def _advertise(self, interval_us=3000000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

        
def demo():
    # Initialise pins
    turnoff = machine.Pin(16, machine.Pin.OUT)
    ds_pin = machine.Pin(15)
    
    # Get voltage
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    machine.Pin(25, mode=machine.Pin.OUT, pull=machine.Pin.PULL_DOWN).high()
    machine.Pin(29, machine.Pin.IN)
    vsys = machine.ADC(29)
    voltage = vsys.read_u16()*3.46*3/65535
    
    
    # Get temperature
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    rom = ds_sensor.scan()[0]
    ds_sensor.convert_temp()
    time.sleep(1)
    tempC = ds_sensor.read_temp(rom)
    print('temperature (ºC):', "{:.2f}".format(tempC))
    
    # Beacon
    ble = bluetooth.BLE()
    temp = BLETemperature(ble, voltage, tempC)
    time.sleep(0.5)
    
    # Signal to turn off
    turnoff.off()
    turnoff.on()
        

if __name__ == "__main__":
    demo()





