from gpiozero import LED
from signal import pause

led = LED(23) # 4, 5, 6, 22, 23, 24, 25, 27 are all unused for comms 
led.blink(on_time=1.0, off_time=1.0)
pause()
