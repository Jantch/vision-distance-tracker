import time

class FPSCounter():
    def __init__(self):
        self.prev_frame_time = 0

    def get_fps(self) -> int:
        new_frame_time = time.time()
        if self.prev_frame_time != 0:
            fps = int(1 / (new_frame_time - self.prev_frame_time))
        else:
            fps = 0

        self.prev_frame_time = new_frame_time
        return fps