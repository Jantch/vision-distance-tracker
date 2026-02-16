import time as t

class PostureTracker():
    def __init__(self, alpha : float = 0.8, if_calibrated : bool = False, interval:float = 0.2):
        self.healthy_pos = None
        self.alpha = alpha
        self.if_calibrated = if_calibrated
        self.last_pos = 0
        self.betha = 0.3
        self.last_update_time = 0 # [s]
        self.update_interval = interval #[s]

    def check_pos(self, rey:float, ley:float) -> float:
        av_pos = (rey + ley) / 2
        self.last_pos = av_pos
        return av_pos

    def if_bad(self) -> bool:
        return (self.last_pos - self.healthy_pos) / self.healthy_pos > self.betha

    def get_last_update_time(self) -> float:
        return self.last_update_time

    def time_update(self):
        self.last_update_time = t.time()

    def should_calculate(self) -> bool:
        return t.time() - self.last_update_time >= self.update_interval and self.if_calibrated

    def calibrate(self) -> None:
        self.healthy_pos = self.last_pos
        self.if_calibrated = True

    def get_healthy_pos(self) -> float:
        return self.healthy_pos

    def get_status(self) -> bool:
        return self.if_calibrated

def pos_t_calibration(pt : PostureTracker, rey : float, ley : float) -> None:
    #if_ready = input("Please sit up straight in front of your camera and enter s when ready.")
    #while if_ready != 's':
        #if_ready = input("Please sit up straight in front of your camera and enter s when ready.")

    #if if_ready == 's':
        pt.check_pos(rey, ley)
        pt.calibrate()

