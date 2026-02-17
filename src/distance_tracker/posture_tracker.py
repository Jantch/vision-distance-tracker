import time as t

class PostureTracker():
    def __init__(self, alpha : float = 0.8, if_calibrated : bool = False, interval:float = 0.2):
        self.healthy_index = None
        self.alpha = alpha
        self.if_calibrated = if_calibrated
        self.last_index = 0
        self.betha = 0.4
        self.last_update_time = 0 # [s]
        self.update_interval = interval #[s]

    def check_pos(self, rey:float, ley:float, curr_dist:float) -> float:
        av_y = (rey + ley) / 2
        act_index = av_y / curr_dist
        self.last_index = act_index
        return self.last_index

    def if_bad(self) -> bool:
        return (self.last_index - self.healthy_index) / self.healthy_index > self.betha

    def get_last_update_time(self) -> float:
        return self.last_update_time

    def time_update(self):
        self.last_update_time = t.time()

    def should_calculate(self) -> bool:
        return t.time() - self.last_update_time >= self.update_interval and self.if_calibrated

    def calibrate(self) -> None:
        self.healthy_index = self.last_index
        self.if_calibrated = True

    def get_healthy_pos(self) -> float:
        return self.healthy_index

    def get_status(self) -> bool:
        return self.if_calibrated

def pos_t_calibration(pt : PostureTracker, rey : float, ley : float, curr_dist:float) -> None:
    #if_ready = input("Please sit up straight in front of your camera and enter s when ready.")
    #while if_ready != 's':
        #if_ready = input("Please sit up straight in front of your camera and enter s when ready.")

    #if if_ready == 's':
        pt.check_pos(rey, ley, curr_dist)
        pt.calibrate()

