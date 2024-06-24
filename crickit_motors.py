import time
import signal
import sys
from adafruit_crickit import crickit

print("DC Motor 1 Test")
motor_1 = crickit.dc_motor_1

def signal_handler(sig, frame):
	print("Set DC throttle to zero")
	motor_1.throttle = 0
	print("\nGoodbye")
	sys.exit(0)
	
signal.signal(signal.SIGINT, signal_handler)

print("Servo Angle Test")
servos = [crickit.servo_1,crickit.servo_2]
crickit.servo_1.set_pulse_width_range(min_pulse=460, max_pulse=2560)


while True:
	
	motor_1.throttle = 1  # dc motor full speed forward
	for servo in servos:
		servo.angle = 0
	time.sleep(2)
	
	motor_1.throttle = 0.5  #dc motor half speed forward
	for servo in servos:
		servo.angle = 180
	time.sleep(2)

