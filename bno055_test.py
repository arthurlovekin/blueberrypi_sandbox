import adafruit_bno055
import board
import time 

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
	try:
		print(sensor.temperature)
		print(sensor.euler)
		print(sensor.gravity)
	except OSError:
		print("Failed to connect. Retrying")
	time.sleep(2)
# TODO sometimes when it loses connection and reconnects the 
# IMU just sends zeros
