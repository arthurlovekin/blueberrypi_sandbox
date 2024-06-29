import asyncio
import evdev

import time
import signal
import sys
from adafruit_crickit import crickit

joystick_map = {
      "FRONT_SERVO":"ABS_Y",

}
### DC Motor
motor_1 = crickit.dc_motor_1

def signal_handler(sig, frame):
	print("Set DC throttle to zero")
	motor_1.throttle = 0
	print("\nGoodbye")
	sys.exit(0)
	
signal.signal(signal.SIGINT, signal_handler)

### Servos
servos = [crickit.servo_1,crickit.servo_2]
crickit.servo_1.set_pulse_width_range(min_pulse=460, max_pulse=2300)
crickit.servo_2.set_pulse_width_range(min_pulse=470, max_pulse=2300)

### Joystick
## Get the device corresponding to the joystick
# devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
# print("--- Available devices ---")
# for device in devices:
#    print(device.path, device.name, device.phys)
# print("-------")
device = evdev.InputDevice('/dev/input/event10')
# print(f"{device=}")
# print("---device capabilities---")
# print(device.capabilities(verbose=True))

## Concurrently handle joystick inputs
async def main(device):
    async for event in device.async_read_loop():
        # if event.type == evdev.ecodes.EV_KEY:
            if event.code == evdev.ecodes.BTN_TL2:
                print("Got BTN_TL2")
            elif event.code == evdev.ecodes.BTN_TR2:
                print("Got BTN_TR2")        
        # elif event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_X:
                print("Got ABS_X")
            elif event.code == evdev.ecodes.ABS_Y:
                print("Got ABS_Y")
            elif event.code == evdev.ecodes.ABS_RX:
                motor_1.throttle = event.value



while True:
	

	for servo in servos:
		servo.angle = 0
	time.sleep(2)
	
	motor_1.throttle = 0.5  #dc motor half speed forward
	for servo in servos:
		servo.angle = 180
	time.sleep(2)

if __name__ == "__main__":
    asyncio.run(main(device))
