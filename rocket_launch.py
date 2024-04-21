from rocket_camera import RocketCamera
from time import sleep
from gpiozero import Buzzer
# from signal import pause

buzz = Buzzer(23) # 4, 5, 6, 22, 23, 24, 25, 27 are all unused for comms 
buzz.beep(on_time=1.0, off_time=2.0)

"""
Take videos with each camera simultaneously
https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf page 21-23 
https://samirkumardas.github.io/jmuxer/h264_player.html is a good online playback tool
ffplay <filename> is a good commandline tool (though was playing at double speed).

playback h264 video with: https://samirkumardas.github.io/jmuxer/h264_player.html
Run this script on startup by creating a file called rocket_launch.service in /lib/systemd/system
that contains:

[Unit]
Description=Run Python Script that controls a rocket
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c '/usr/bin/python3 /home/arthur/sandbox/rocket_launch.py > /home/arthur/Videos/rocket_launch.log 2>&1'

[Install]
WantedBy=multi-user.target

"""
#
print("Starting Cameras ...")
try:
    cam0 = RocketCamera(0)
    cam0.start_recording_including_buffer()
except:
    print("Camera 0 not found")
try:
    cam1 = RocketCamera(1)
    cam1.start_recording_including_buffer()
except:
    print("Camera 1 not found")

for i in range(10*60):
    print(f"Rocket Flying {i}...")
    sleep(1)

print("Stop Recording")
try:
    cam0.stop_recording()
except:
    print("Camera 0 couldn't stop recording")
try:
    cam1.stop_recording()
except:
    print("Camera 1 couldn't stop recording")

buzz.beep(on_time=0.5, off_time=0.5)
for i in range(20*60):
    print(f"Rocket Landed. {i}...")
    sleep(1)

print('Flight Complete')

# For Rocket TODO: 
"""
7.2.3. CircularOutput
The CircularOutput class is derived from the FileOutput and adds the ability to start a recording with video frames that
were from several seconds earlier.
""" 
# Connect the recording to a trigger from the IMU.