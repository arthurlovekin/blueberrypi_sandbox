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
                print("Got BTN_TL2")
            elif event.code == evdev.ecodes.BTN_TR2:
                print("Got BTN_TR2")        
        
        elif event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_X:
                print("Got ABS_X")
            elif event.code == evdev.ecodes.ABS_Y:
                print("Got ABS_Y")
            elif event.code == evdev.ecodes.ABS_RX:
                print("Got ABS_RX")
            print(f"{evdev.categorize(event)} : {event.value}")
        # print(repr(event))

if __name__ == "__main__":
    asyncio.run(main(device))
