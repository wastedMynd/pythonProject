import time

class Camera(object):
    def __init__(self):
        self.frame_count = 3
        self.frames = [
            open(f'{frame}.jpg', 'rb').read() for frame in range(self.frame_count)
        ]

    def get_frame(self):
        return self.frames[int(time.time()) % self.frame_count]

