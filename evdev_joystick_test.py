import asyncio
import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
print("--- Available devices ---")
for device in devices:
   print(device.path, device.name, device.phys)
print("-------")
device = evdev.InputDevice('/dev/input/event10')
print(f"{device=}")
print("---device capabilities---")

print(device.capabilities(verbose=True))
print(f"AbsInfo: {device.absinfo(evdev.ecodes.ABS_X)}")
print(f"Min: {device.absinfo(evdev.ecodes.ABS_X).min}, Max: {device.absinfo(evdev.ecodes.ABS_X).max}")

# Map from value v, which lies in range [vmin, vmax], 
# to an output that lies in range [out_min, out_max]
def linear_map(v, vmin, vmax, out_min, out_max):
    return (float(v)-float(vmin)) / (float(vmax)-float(vmin)) * (float(out_max) - float(out_min)) + float(out_min)

## if you want without asyncio
# for event in device.read_loop():
#     if event.type == evdev.ecodes.EV_KEY:
#         print(evdev.categorize(event)) # categorize gives a timestamp and the button type
#     elif event.type == evdev.ecodes.EV_ABS:
#         print(f"{evdev.categorize(event)} : {event.value}")

async def main(device):
    async for event in device.async_read_loop():
        # types (event_factory): 0: SyncEvent; 1: KeyEvent; 2: RelEvent, 3: AbsEvent
        if event.type == evdev.ecodes.EV_KEY:
            # print(f"{event.type=} {event.timestamp()} {event.code=}~{evdev.resolve_ecodes(evdev.ecodes.BTN, [event.code])} {event.value=}")
            print(f"{evdev.categorize(event)} : {event.value}") # categorize gives a timestamp and the button type
            if event.code == evdev.ecodes.BTN_TL2:
                print(f"Got BTN_TL2: {event.value}")
            elif event.code == evdev.ecodes.BTN_TR2:
                print(f"Got BTN_TR2: {event.value}")        
        
        elif event.type == evdev.ecodes.EV_ABS:
            abs_min = device.absinfo(evdev.ecodes.ABS_X).min
            abs_max = device.absinfo(evdev.ecodes.ABS_X).max
            if event.code == evdev.ecodes.ABS_X:
                angle = linear_map(event.value, abs_min, abs_max, 0.0, 180.0)
                print(f"ABS_X: {event.value} -> angle: {angle}")
            elif event.code == evdev.ecodes.ABS_Y:
                throttle = -1.0 * linear_map(event.value, abs_min, abs_max, -1.0, 1.0)
                print(f"ABS_Y: {event.value} -> throttle: {throttle}")
            elif event.code == evdev.ecodes.ABS_RX:
                print("Got ABS_RX")
            print(f"{evdev.categorize(event)} : {event.value}")
        # print(repr(event))

if __name__ == "__main__":
    asyncio.run(main(device))
