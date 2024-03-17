from picamera2 import Picamera2, Preview
from time import sleep
from picamera2.encoders import H264Encoder, MJPEGEncoder
from libcamera import Transform

# https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf page 21-23 
# Take videos with each camera simultaneously

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
config0 = picam0.create_video_configuration(sensor={'output_size':(2304,1296), 'bit_depth':10})
picam0.configure(config0)
# get the same configuration a different way
mode1 = picam1.sensor_modes[1]
config1 = picam1.create_video_configuration(sensor={'output_size':mode1['size'], 'bit_depth':mode1['bit_depth']})
picam1.configure(config1)
# Could always record at a lower framerate if desired (eg. 25fps)
# config = picam2.create_video_configuration(controls={"FrameDurationLimits": (40000, 40000)})

# Can this encoder handle 2 cameras at 60fps with 1080p? Probably not.
encoder0 = H264Encoder(bitrate=10000000)
encoder1 = H264Encoder(bitrate=10000000)
output_file0 = "results/cam0.h264"
output_file1 = "results/cam1.h264"
# encoder0 = MJPEGEncoder()
# encoder1 = MJPEGEncoder()
# output_file0 = "cam0.mjpg"
# output_file1 = "cam1.mjpg"

for i in range(5,0,-1):
    print(f"Video in {i}...")
    sleep(1)

picam0.start_encoder(encoder0, output_file0)
picam0.start()
picam1.start_recording(encoder1, output_file1)

sleep(5)
picam0.stop()
picam0.stop_encoder()
picam1.stop_recording()

picam0.stop_preview()
picam1.stop_preview()


# For Rocket TODO: 
"""
7.2.3. CircularOutput
The CircularOutput class is derived from the FileOutput and adds the ability to start a recording with video frames that
were from several seconds earlier.
Connect the recording to a trigger from the IMU.
"""