#!/usr/bin/env python3

import smbus2

# Define I2C bus
DEVICE_BUS = 1

# Define device i2c slave address.
DEVICE_ADDR = 0x17

# Set the threshold of UPS automatic power-off to prevent damage caused by battery over-discharge, unit: mV.
FULL_VOLT = 4200
PROTECT_VOLT = 2700
EMPTY_VOLT = 2500

# Raspberry Pi Communicates with MCU via i2c protocol.
bus = smbus2.SMBus(DEVICE_BUS)

# Set Full voltage 0x0D - 0x0E	13 - 14
bus.write_byte_data(DEVICE_ADDR, 13, FULL_VOLT & 0xFF)
bus.write_byte_data(DEVICE_ADDR, 14, (FULL_VOLT >> 8)& 0xFF)

# Set Protect voltage 0x11 - 0x12	17 - 18
bus.write_byte_data(DEVICE_ADDR, 17, PROTECT_VOLT & 0xFF)
bus.write_byte_data(DEVICE_ADDR, 18, (PROTECT_VOLT >> 8)& 0xFF)

# Set Empty voltage 0x0F - 0x10	15 - 16
bus.write_byte_data(DEVICE_ADDR, 15, EMPTY_VOLT & 0xFF)
bus.write_byte_data(DEVICE_ADDR, 16, (EMPTY_VOLT >> 8)& 0xFF)

# Set Battery Parameters self-programmed by user 0x2A	42
bus.write_byte_data(DEVICE_ADDR, 42, 1 & 0xFF)

# Read register and add the data to the list: aReceiveBuf
aReceiveBuf = []
aReceiveBuf.append(0x00)
for i in range(1, 255):
    aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

set_full_voltage = (aReceiveBuf[14] << 8 | aReceiveBuf[13])
set_protect_voltage = (aReceiveBuf[18] << 8 | aReceiveBuf[17])
set_empty_voltage = (aReceiveBuf[16] << 8 | aReceiveBuf[15])

user_Parameter_activated = aReceiveBuf[42]

print("Full battery voltage set to: %d mV"% (aReceiveBuf[14] << 8 | aReceiveBuf[13]))
print("Battery empty voltage set to: %d mV"% (aReceiveBuf[16] << 8 | aReceiveBuf[15]))
print("Battery protection voltage set to: %d mV"% (aReceiveBuf[18] << 8 | aReceiveBuf[17]))
print("User Parameter for Batterie is set: %d (1 = True)"%user_Parameter_activated)
