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


for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        print(evdev.categorize(event)) # categorize gives a timestamp and the button type
    elif event.type == evdev.ecodes.EV_ABS:
        print(f"{evdev.categorize(event)} : {event.value}")
