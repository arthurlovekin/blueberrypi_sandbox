from picamera2 import Picamera2, Preview
from time import sleep
from picamera2.encoders import H264Encoder, MJPEGEncoder
from libcamera import Transform
from time import sleep, localtime, strftime

"""
Testing different framerates and ecnoding types to see how much memory it takes and how good the quality is.
https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf page 21-23 

ffplay 2024-03-31_11-35-00_cam0.mjpg
"""

# create camera objects
picam0 = Picamera2(0)

# start a preview window
picam0.start_preview(Preview.QTGL,
                     x=100, 
                     y=200, 
                     width=800, 
                     height=600,
                     transform=Transform(hflip=False))

# Set configuration for video
"""
>>> from pprint import *
>>> from picamera2 import Picamera2
>>> picam2 = Picamera2()
>>> pprint(picam2.sensor_modes)
[{'bit_depth': 10,
  'crop_limits': (768, 432, 3072, 1728),
  'exposure_limits': (9, None),
  'format': SRGGB10_CSI2P,
  'fps': 120.13,
  'size': (1536, 864),
  'unpacked': 'SRGGB10'},
 {'bit_depth': 10,
  'crop_limits': (0, 0, 4608, 2592),
  'exposure_limits': (13, 77208384, None),
  'format': SRGGB10_CSI2P,
  'fps': 56.03,
  'size': (2304, 1296),
  'unpacked': 'SRGGB10'},
 {'bit_depth': 10,
  'crop_limits': (0, 0, 4608, 2592),
  'exposure_limits': (26, 112015443, None),
  'format': SRGGB10_CSI2P,
  'fps': 14.35,
  'size': (4608, 2592),
  'unpacked': 'SRGGB10'}]
"""
config = picam0.create_video_configuration(sensor={'output_size':(2304,1296), 'bit_depth':10})#,
                                            # controls={"FrameDurationLimits": (40000,40000)}) # Lower to 25 fps
picam0.configure(config)
# Could always record at a lower framerate if desired (eg. 25fps)
# config = picam2.create_video_configuration(controls={"FrameDurationLimits": (40000, 40000)})

"""
A 5 second video 
  at ~60fps occupied
    2.3MiB for mjpg
    6.2 MiB for h264
  at ~25fps occupied
    2.6 MiB for mjpg (setting controls=FrameDuration didn't help for some reason)

"""

# # Can this encoder handle 2 cameras at 60fps with 1080p? Probably not.
# encoder = H264Encoder(bitrate=10000000)
encoder = MJPEGEncoder()
time_str = strftime(f"%Y-%m-%d_%H-%M-%S", localtime())
output_file = f"results/{time_str}_cam.mjpg"

for i in range(5,0,-1):
    print(f"Video in {i}...")
    sleep(1)


picam0.start_recording(encoder, output_file)

sleep(5)

picam0.stop_recording()
picam0.stop_preview()


# For Rocket TODO: 
"""
7.2.3. CircularOutput
The CircularOutput class is derived from the FileOutput and adds the ability to start a recording with video frames that
were from several seconds earlier.
Connect the recording to a trigger from the IMU.
"""