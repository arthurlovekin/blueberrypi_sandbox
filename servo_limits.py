import time
import signal
import sys
from adafruit_crickit import crickit

def signal_handler(sig, frame):
	print("\nGoodbye")
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

print("Servo Angle Test")
servos = [crickit.servo_1,crickit.servo_2]
crickit.servo_1.set_pulse_width_range(min_pulse=460, max_pulse=2560)
while True:
	for servo in servos:
		servo.angle = 0
	time.sleep(2)

	for servo in servos:
		servo.angle = 180
	time.sleep(2)

