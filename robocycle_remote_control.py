import asyncio
import evdev

import time
import signal
import sys
from adafruit_crickit import crickit

# Map from value v, which lies in range [vmin, vmax], 
# to an output that lies in range [out_min, out_max]
def linear_map(v, vmin, vmax, out_min, out_max):
    return (float(v)-float(vmin)) / (float(vmax)-float(vmin)) * (float(out_max) - float(out_min)) + float(out_min)

## Concurrently handle joystick inputs
async def main(device):
    async for event in device.async_read_loop():
        if (event.code == evdev.ecodes.BTN_TL2 or 
            event.code == evdev.ecodes.BTN_TR2): # Enable
            motors_enabled = bool(event.value)
            print(f"BTN_TL2 or BTN_TR2: {event.value} -> {motors_enabled=}")
        if motors_enabled:
            if event.code == evdev.ecodes.ABS_X: # front servo (steering)
                crickit.servo_1.angle = linear_map(event.value, abs_x_min, abs_x_max, 0.0, 180.0)
                print(f"ABS_X: {event.value} -> angle: {crickit.servo_1.angle}")
            elif event.code == evdev.ecodes.ABS_Y: # DC Motor (speed)
                motor_1.throttle = -1.0*linear_map(event.value, abs_y_min, abs_y_max, -1.0,1.0)
                print(f"ABS_Y: {event.value} -> throttle: {motor_1.throttle}")
            elif event.code == evdev.ecodes.ABS_RX: # Body Servo
                crickit.servo_2.angle = linear_map(event.value, abs_Rx_min, abs_Rx_max, 0.0, 180.0)
                print(f"ABS_RX: {event.value} -> angle: {crickit.servo_2.angle}")
        else:
            print("Motors disabled. Inputs not being read")

if __name__ == "__main__":
    motors_enabled = False

    ### DC Motor
    motor_1 = crickit.dc_motor_1

    def signal_handler(sig, frame):
        print("Set DC throttle to zero")
        motor_1.throttle = 0
        print("\nGoodbye")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    ### Servos
    crickit.servo_1.set_pulse_width_range(min_pulse=470, max_pulse=2300)
    crickit.servo_2.set_pulse_width_range(min_pulse=470, max_pulse=2300)

    ### Joystick
    device = evdev.InputDevice('/dev/input/event10')
    abs_x_min = device.absinfo(evdev.ecodes.ABS_X).min
    abs_x_max = device.absinfo(evdev.ecodes.ABS_X).max
    abs_y_min = device.absinfo(evdev.ecodes.ABS_Y).min
    abs_y_max = device.absinfo(evdev.ecodes.ABS_Y).max
    abs_Rx_min = device.absinfo(evdev.ecodes.ABS_RX).min
    abs_Rx_max = device.absinfo(evdev.ecodes.ABS_RX).max

    asyncio.run(main(device))
