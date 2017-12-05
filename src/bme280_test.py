import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus, address)

data = bme280.sample(bus, address)

print data

