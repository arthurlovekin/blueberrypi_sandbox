import time
import signal
import sys
from adafruit_crickit import crickit

def signal_handler(sig, frame):
	print("\nGoodbye")
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

print("2 Servo demo!")
servos = (crickit.servo_1, crickit.servo_2)

t0_s = time.time() # float seconds since epoch
t1_s = float('-inf') # seconds since last update
dt_s = 0.001 # sets total loop rate
trajectory = [(90.0,0.0),(90.0,1.0),(0.0,3.0),(0.0,4.0),(90.0,6.0),(180.0,9.0), (180.0,12.0)] # (degrees, seconds)

while True:	
	t = time.time() - t0_s
	if t - t1_s < dt_s:
		continue
	t1_s = t
	for (ai,ti),(aj,tj) in zip(trajectory[:-1],trajectory[1:]):
		if t > ti and t < tj:
			crickit.servo_1.angle = (t - ti)/(tj-ti)*(aj-ai)+ai	
			break

