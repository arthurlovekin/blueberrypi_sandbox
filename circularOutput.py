from picamera2.encoders import H264Encoder, MJPEGEncoder, Quality
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
from time import sleep

"""
Summary: Both Encoders work with the CircularOutput (one camera)
The encoders in both cases seem to be limited to 30fps:
    With the MJPEGEncoder playback was normal speed (maybe slightly slow)
     but the default buffer of 150 led to a 5 second buffer indicating 30fps
    With the H264Encoder the playback is double-speed and
     the default buffer of 150 led to a 5 second buffer indicating 30fps
File Size
    15 s video, controls={"FrameDurationLimits" --> 30fps, h264 8.2 MiB
    15 s video, controls={"FrameDurationLimits" --> 30fps, mjpg 10.5MiB
    15 s video, h264 8.3 MiB
    15 s video, mjpg 10.3
    5 s video h264 6.2
    5 s video mjpg 2.3

Use h264 bacuase it is better at compressing long videos (but not short ones).
FrameDurationLimits seem to improve storage slightly for h264 but make it worse for mjpg
(This probably limits the framerate to match what the encoder can handle)
"""

picam2 = Picamera2(0)
config = picam2.create_video_configuration(sensor={'output_size':(2304,1296), 'bit_depth':10},
                                            controls={"FrameDurationLimits": (33333,33333)}) # Lower to 30 fps
picam2.configure(config)

encoder = H264Encoder() #MJPEGEncoder() #
output = CircularOutput() #use the default buffer_size=150 (3sec at 30fps)
picam2.start_recording(encoder, output, quality=Quality.MEDIUM)
print("Phase 1: On the launchpad...")
for i in range(10,0,-1):
    print(f"Launch in {i}...")
    sleep(1)
print("Rocket Launch!")

# Now when it's time to start recording the output, including the previous 5 seconds:
# output.fileoutput = "results/file30.mjpg" 
output.fileoutput = "results/file30.h264"
output.start()
for i in range(5,0,-1):
    print(f"Phase 2: Rocket Flying {i}...")
    sleep(1)
print("Rocket landed")
for i in range(5,0,-1):
    print(f"Phase 3: Sitting on the ground {i}...")
    sleep(1)
print("End of recording")
# And later it can be stopped with:
output.stop()

sleep(5)

picam2.stop_recording()
picam2.stop_preview()

