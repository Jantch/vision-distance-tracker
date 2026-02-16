import numpy as np
import time as t

class HeadPoseTracker:
    def __init__(self, interval : float = 0.2):
        file_path = None
        self.last_update_time = 0 # [s]
        self.update_interval = interval #[s]

    def calculate_angle(self, rex, rey, lex, ley):
        b = rex - lex
        a = ley - rey
        alpha = np.atan2(a, b)
        return alpha*(180/np.pi)

    def get_last_update_time(self) -> float:
        return self.last_update_time

    def time_update(self):
        self.last_update_time = t.time()

    def should_calculate(self) -> bool:
        return t.time() - self.last_update_time >= self.update_interval