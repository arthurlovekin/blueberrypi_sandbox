from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import CircularOutput
from time import localtime, strftime
from pathlib import Path

class RocketCamera():
    def __init__(self, port_index, name=None, output_file=None):
        self.index = port_index
        self.name = name if name is not None else f"cam{port_index}"
        time_str = strftime(f"%Y-%m-%d_%H-%M-%S", localtime())
        # new_output_file = Path(Path.home(), "Videos", f"{time_str}_{self.name}.h264")
        new_output_file = Path("home", "arthur", "Videos", f"{time_str}_{self.name}.h264")
        self.output_file = output_file if output_file is not None else new_output_file
        self.picam = Picamera2(self.index)

        config = self.picam.create_video_configuration(sensor={'output_size':(2304,1296), 'bit_depth':10},
                                                    controls={"FrameDurationLimits": (33333,33333)}) # Lower to 30 fps
        self.picam.configure(config)

        self.encoder = H264Encoder() 
        self.output = CircularOutput() #use the default buffer_size=150 (3sec at 30fps)
        self.picam.start_recording(self.encoder, self.output, quality=Quality.MEDIUM)

    def start_recording_including_buffer(self):
        self.output.fileoutput = self.output_file
        self.output.start()
        print(f"RocketCamera: {self.name} Recording Started...")

    def stop_recording(self):
        self.output.stop()
        self.picam.stop_recording()
        print(f"RocketCamera: Saved {self.name} video to {self.output_file}")
