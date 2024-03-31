from picamera2 import Picamera2
from time import sleep, localtime, strftime
from picamera2.encoders import MJPEGEncoder

time_str = strftime(f"%Y-%m-%d_%H-%M-%S", localtime())
output_file0 = f"results/{time_str}_cam0.mjpg"
output_file1 = f"results/{time_str}_cam1.mjpg"

picam0 = Picamera2(0)
picam1 = Picamera2(1)

config0 = picam0.create_video_configuration(sensor={'output_size':(2304,1296), 'bit_depth':10})
picam0.configure(config0)
config1 = picam1.create_video_configuration(sensor={'output_size':(2304,1296), 'bit_depth':10})
picam1.configure(config1)

encoder0 = MJPEGEncoder()
encoder1 = MJPEGEncoder()

picam0.start_recording(encoder0, output_file0)
picam1.start_recording(encoder1, output_file1)

sleep(5)
picam0.stop_recording()
picam1.stop_recording()


# For Rocket TODO: 
"""
7.2.3. CircularOutput
The CircularOutput class is derived from the FileOutput and adds the ability to start a recording with video frames that
were from several seconds earlier.
Connect the recording to a trigger from the IMU.
"""