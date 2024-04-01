from rocket_camera import RocketCamera
from time import sleep

"""
Take videos with each camera simultaneously
https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf page 21-23 
https://samirkumardas.github.io/jmuxer/h264_player.html is a good online playback tool
ffplay <filename> is a good commandline tool (though was playing at double speed).
"""
#
print("Starting Cameras ...")
cam0 = RocketCamera(0)
cam1 = RocketCamera(1)

cam0.start_recording_including_buffer()
cam1.start_recording_including_buffer()

for i in range(15,0,-1):
    print(f"Rocket Flying {i}...")
    sleep(1)

cam0.stop_recording()
cam1.stop_recording()

# For Rocket TODO: 
"""
7.2.3. CircularOutput
The CircularOutput class is derived from the FileOutput and adds the ability to start a recording with video frames that
were from several seconds earlier.
Connect the recording to a trigger from the IMU.
"""