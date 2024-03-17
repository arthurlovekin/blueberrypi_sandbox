from picamera2 import Picamera2, Preview
from time import sleep
from libcamera import Transform
# https://www.tomshardware.com/raspberry-pi/how-to-use-dual-cameras-on-the-raspberry-pi-5
# Take pictures with each camera simultaneously

# create camera objects
picam0 = Picamera2(0)
picam1 = Picamera2(1)

# start a preview window
picam0.start_preview(Preview.QTGL,
                     x=100, 
                     y=200, 
                     width=800, 
                     height=600,
                     transform=Transform(hflip=False))
picam1.start_preview(Preview.QTGL)

picam0.start()
picam1.start()

for i in range(10,0,-1):
    print(f"Image in {i}...")
    sleep(1)

picam0.capture_file("results/cam0.jpg")
picam1.capture_file("results/cam1.jpg")

picam0.stop()
picam1.stop()

picam0.stop_preview()
picam1.stop_preview()

