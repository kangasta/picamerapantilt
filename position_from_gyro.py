#!/usr/bin/env python3

from mpu6050 import mpu6050
sensor = mpu6050(0x68)

data = sensor.get_gyro_data()
for field in sorted(data):
	print(str(field) + ": " + str(data[field]))